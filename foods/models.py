import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, REAL, CHAR, VARCHAR, TIMESTAMP, TEXT, ForeignKey
import json
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from extentions import db, elastic
from wtforms import SelectField


class SearchableMixin(object):

    @classmethod
    def add_to_index(cls, instance):
        if elastic is None:
            return
        if not hasattr(instance, 'elastic_document'):
            raise Exception("model doesn't have 'elastic_document' attribute")

        payload = instance.elastic_document
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
        search = elastic.search(
            index=cls.__indexname__,
            body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                  'from': (page - 1) * per_page, 'size': per_page})
        ids = [int(hit['_id']) for hit in search['hits']['hits']]
        return ids, search['hits']['total']['value']

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
    def reindex(cls):
        for obj in cls.query:
            cls.add_to_index(obj)


class Food(db.Model,SearchableMixin):
    __tablename__ = 'foods'
    __indexname__ = 'foods'

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
            return payload

    def __repr__(self):
        return f"<Food '{self.Title}'>"

    @property
    def simple_view(self) -> dict:
        """
               a simple view of food model
        """
        return {
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
            'tag_cloud': recipe['tag_cloud'],
            'ingredients': [ingredient['food']['food_name'] for ingredient in recipe['ingredients']],
            'directions': [direction['text'] for direction in recipe['directions']]
        }

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


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)