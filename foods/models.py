import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, REAL, CHAR, VARCHAR, TIMESTAMP, TEXT, ForeignKey
import json
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
from extentions import db
from wtforms import SelectField


class Food(db.Model):
    __tablename__ = 'foods'

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
    def recipe(self):
        if self.Recipe is None or self.Recipe == '':
            return None
        else:
            payload = json.loads(self.Recipe)
            payload['category'] = self.Category
            payload['date_created'] = self.CreatedAt.strftime('%Y-%m-%d %H:%M:%S')
            return payload

    def __repr__(self):
        return f"<Food '{self.Title}'>"

    @property
    def simple_view(self):
        """
               a simple view of food model
        """
        return {
            'id': self.id,
            'category': self.Category,
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

    def get_calorie(self):
        return self.Calories


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
