from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from extentions import db


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, unique=True) 
    summary = Column(String(256), nullable=True, unique=False)
    content = Column(Text, nullable=False, unique=False)
    slug = Column(String(128), nullable=False, unique=True)
    category = Column(String(256), nullable=True, unique=False)
    author = Column(Integer, db.ForeignKey('users.id'), nullable=False)
