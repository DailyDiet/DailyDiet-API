import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, REAL, CHAR, VARCHAR, TIMESTAMP, TEXT, ForeignKey, JSON
import json
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from config import Config
from extentions import db, elastic
from wtforms import SelectField
from elasticsearch_dsl import Q, Search


def build_query(input_json):
    query = {}
    if input_json.get('text') is not None and input_json['text'] != '':
        query['should'] = [
            {
                "multi_match": {
                    "query": input_json['text'],
                    "fields": [
                        "name^6.0",
                        "category^1.0",
                        "description^3.0",
                        "tag_cloud^3.0",
                        "ingredients^2.0",
                        "directions^1.5",
                        "author^1.0"
                    ],
                    "type": "phrase_prefix",
                    "lenient": "true"
                }
            },
        ]
        query['boost'] = 1
        query['minimum_should_match'] = 1

    # building must query
    if input_json.get('category') is not None:
        if query.get('must') is None:
            query['must'] = []
        query['must'].append({
            "match": {
                "category": input_json['category']
            }
        })

    for feature in ["calories", "carbs", "fats", "proteins"]:
        if input_json.get(feature) is not None:
            if query.get('must') is None:
                query['must'] = []
            part = {
                'range':{}
            }
            if input_json[feature].get('min') is not None or input_json[feature].get('max') is not None:
                if input_json[feature].get('min') is not None:
                    if part['range'].get(f'nutrition.{feature}') is None:
                        part['range'][f'nutrition.{feature}'] = {}
                    part['range'][f'nutrition.{feature}']['gte'] = input_json[feature]['min']
                if input_json[feature].get('max') is not None:
                    if part['range'].get(f'nutrition.{feature}') is None:
                        part['range'][f'nutrition.{feature}'] = {}
                    part['range'][f'nutrition.{feature}']['lte'] = input_json[feature]['min']
                query['must'].append(part)

    for feature in ["cook_time", "prep_time", "total_time"]:
        if input_json.get(feature) is not None:
            if query.get('must') is None:
                query['must'] = []
            part = {
                'range': {}
            }
            if input_json[feature].get('min') is not None or input_json[feature].get('max') is not None:
                if input_json[feature].get('min') is not None:
                    if part['range'].get(feature) is None:
                        part['range'][feature] = {}
                    part['range'][feature]['gte'] = input_json[feature]['min']
                if input_json[feature].get('max') is not None:
                    if part['range'].get(feature) is None:
                        part['range'][feature] = {}
                    part['range'][feature]['lte'] = input_json[feature]['min']
                query['must'].append(part)

    return query


class SearchTimedOutException(Exception):
    pass


class SearchableMixin(object):

    @classmethod
    def add_to_index(cls, instance):
        if elastic is None:
            return
        if not hasattr(instance, 'elastic_document'):
            raise Exception("model doesn't have 'elastic_document' attribute")

        payload = instance.elastic_document

        if not hasattr(instance, 'ingredients_summery'):
            raise Exception("model doesn't have 'ingredients_summery' attribute")
        ingredients = instance.ingredients_summery

        if not hasattr(cls, '__ingredients_index__'):
            raise Exception("class doesn't have '__ingredients_index__' attribute")

        for ingredient_id, ingredient in ingredients.items():
            elastic.index(index=cls.__ingredients_index__, body=ingredient, id=ingredient_id, doc_type='ingredient')

        if not hasattr(cls, '__indexname__'):
            raise Exception("class doesn't have '__indexname__' attribute")
        elastic.index(index=cls.__indexname__, body=payload, id=instance.id)

    @classmethod
    def remove_from_index(cls, instance):
        if elastic is None:
            return
        if not hasattr(cls, '__indexname__'):
            raise Exception("class doesn't have '__indexname__' attribute")

        elastic.delete(index=cls.__indexname__, id=instance.id)

    @classmethod
    def query_index(cls, query, page=1, per_page=10):
        if elastic is None:
            return [], 0
        search = Search(using=elastic, index=cls.__indexname__)
        elastic_query = Q('bool',
                          should=[
                              {
                                  "multi_match": {
                                      "query": query,
                                      "fields": [
                                          "name^6.0",
                                          "category^1.0",
                                          "description^3.0",
                                          "tag_cloud^3.0",
                                          "ingredients^2.0",
                                          "directions^1.5",
                                          "author^1.0"
                                      ],
                                      "type": "phrase_prefix",
                                      "lenient": "true"
                                  }
                              },

                          ],
                          boost=1,
                          minimum_should_match=1)
        from_index = (page - 1) * per_page
        size = per_page
        search = search.query(elastic_query)
        search_results = search[from_index: from_index + size].execute().to_dict()
        if search_results['timed_out']:
            raise SearchTimedOutException()

        ids = [int(hit['_id']) for hit in search_results['hits']['hits']]
        return ids, search_results['hits']['total']['value']

    @classmethod
    def search(cls, expression, page=1, per_page=10):
        ids, total = cls.query_index(expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0  # just returning nothing
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                cls.add_to_index(obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                cls.add_to_index(obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                cls.remove_from_index(obj)
        session._changes = None

    @classmethod
    def ingredient_search(cls, expression, page=1, per_page=10):
        if elastic is None:
            return [], 0
        search_results = elastic.search(
            index='ingredients',
            body={'query': {'multi_match': {'query': expression, 'fields': ['food_name']}},
                  'from': (page - 1) * per_page, 'size': per_page})
        if search_results['timed_out']:
            raise SearchTimedOutException()
        total = search_results['hits']['total']['value']
        return [hit['_source'] for hit in search_results['hits']['hits']], total

    @classmethod
    def advanced_query(cls, input_json):
        if elastic is None:
            return [], 0
        page = 1 if input_json.get('page') is None else input_json['page']
        per_page = 10 if input_json.get('per_page') is None else input_json['per_page']
        search = Search(using=elastic, index=cls.__indexname__)
        elastic_query = Q('bool',**build_query(input_json))
        from_index = (page - 1) * per_page
        size = per_page
        search = search.query(elastic_query)
        if input_json.get('ingredients') is not None:
            for ing_id in input_json['ingredients']:
                search = search.filter('term', ingredient_ids=ing_id)

        search_results = search[from_index: from_index + size].execute().to_dict()

        if search_results['timed_out']:
            raise SearchTimedOutException()
        ids = [int(hit['_id']) for hit in search_results['hits']['hits']]
        return ids, search_results['hits']['total']['value']

    @classmethod
    def advanced_search(cls, input_json):
        ids, total = cls.advanced_query(input_json)
        if total == 0:
            return cls.query.filter_by(id=0), 0  # just returning nothing
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            cls.add_to_index(obj)


class Food(db.Model, SearchableMixin):
    __tablename__ = 'foods'
    __indexname__ = 'foods_new'
    __ingredients_index__ = 'ingredients'

    id = Column('id', Integer(), primary_key=True)
    Calories = Column('calories', Integer())
    Fat = Column('fat', REAL())
    Fiber = Column('fiber', REAL())
    Protein = Column('protein', REAL())
    Category = Column('category', VARCHAR(20), nullable=False)
    Image = Column('image', VARCHAR(400), default=None)
    Thumbnail = Column('thumbnail', VARCHAR(400), default=None)
    Title = Column('title', VARCHAR(200), nullable=False)
    CreatedAt = Column('created_at', TIMESTAMP())
    AuthorId = Column('author', Integer(), ForeignKey('users.id'), nullable=False)

    # should not be accessed directly, use `recipe` property insted
    # this column will be deprecated soon
    Recipe = Column('recipe', TEXT())

    # @hybrid_property
    # def Category(self):
    #     return self._Category.strip()
    #
    # @Category.setter
    # def category_setter(self, category):
    #     self._Category = category

    @property
    def recipe(self) -> dict:
        if self.Recipe is None or self.Recipe == '':
            return None
        else:
            payload = json.loads(self.Recipe)
            payload['category'] = self.get_category()
            payload['date_created'] = self.CreatedAt.strftime('%Y-%m-%d %H:%M:%S')

            # fixing image loss
            if len(payload['images']) != 0 and payload['primary_image'] is None:
                payload['primary_image'] = payload['images'][0]['image']
                payload['primary_thumbnail'] = payload['images'][0]['thumbnail']

            return payload

    def __repr__(self):
        return f"<Food '{self.Title}'>"

    @property
    def simple_view(self) -> dict:
        """
               a simple view of food model
        """
        payload = {
            'id': self.id,
            'category': self.get_category(),
            'image': self.Image,
            'thumbnail': self.Thumbnail,
            'title': self.Title,
            'nutrition': {'calories': self.Calories,
                          'fat': self.Fat,
                          'fiber': self.Fiber,
                          'protein': self.Protein}
        }
        if payload['image'] is None:
            recipe = self.recipe
            payload['image'] = recipe['primary_image']
            payload['thumbnail'] = recipe['primary_thumbnail']

        return payload

    def __str__(self):
        return json.dumps(self.simple_view)

    def get_calorie(self) -> int:
        return self.Calories

    def get_category(self) -> str:
        return self.Category.strip().lower()

    @property
    def elastic_document(self):
        """
        :return: elastic search index document
        """
        recipe = self.recipe
        payload = {
            'author': self.author.FullName,
            'name': recipe['food_name'],
            'description': recipe['description'],
            'category': recipe['category'],
            'nutrition': {key: value / recipe['servings'] for key, value in recipe['nutrition'].items()},
            'tag_cloud': recipe['tag_cloud'],
            'ingredients': [ingredient['food']['food_name'] for ingredient in recipe['ingredients']],
            'ingredient_ids': [ingredient['food']['id'] for ingredient in recipe['ingredients']],
            'directions': [direction['text'] for direction in recipe['directions']],
            'cook_time': recipe['cook_time'],
            'prep_time': recipe['prep_time'],
            'total_time': recipe['cook_time'] + recipe['prep_time']
        }

        return payload

    @property
    def ingredients_summery(self):
        payload = {}
        recipe = self.recipe
        for ingredient in recipe['ingredients']:
            payload[ingredient['food']['id']] = ingredient['food']
        return payload


# for admin integration
class FoodModelView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_exclude_list = ['Recipe']
    column_searchable_list = ['Title', 'Category']
    column_filters = ['Calories', 'Fiber', 'Fat', 'Protein']
    create_modal = True
    edit_modal = True

    form_choices = {
        'Category': [(item, item.replace('_', ' ')) for item in [
            'mostly_meat',
            'appetizers',
            'drink',
            'main_dish',
            'sandwich',
            'dessert',
            'breakfast',
            'protein_shake',
            'salad',
            'pasta'
        ]]
    }


class DietRecord(db.Model):
    id = Column(Integer(), primary_key=True)
    generatedAt = Column('generated_at', TIMESTAMP(), nullable=False, default=datetime.datetime.now)
    ownerId = Column('owner_id', Integer(), ForeignKey('users.id'), nullable=False)
    diet = Column('diet', JSON(), nullable=False)


class DietRecordModelView(ModelView):
    can_edit = True
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_labels = {'generatedAt': 'Generated At', 'diet': 'Diet ids'}


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
