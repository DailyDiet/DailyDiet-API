from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from extentions import db

from flask_admin.contrib.sqla import ModelView

class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, unique=True)
    summary = Column(String(256), nullable=True, unique=False)
    content = Column(Text, nullable=False, unique=False)
    slug = Column(String(128), nullable=False, unique=True)
    category = Column(String(256), nullable=True, unique=False)
    authorId = Column('authorid', Integer(), ForeignKey('users.id'), nullable=False)

class PostModelView(ModelView):
    can_edit = True
    column_display_pk = True
    column_searchable_list = ['title']
