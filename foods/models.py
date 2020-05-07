import datetime

from sqlalchemy import Column, Integer, REAL, CHAR, VARCHAR, TIMESTAMP

from extentions import db


class Food(db.Model):
    __tablename__ = 'foods'

    id = Column('id', Integer(), primary_key=True)
    calories = Column('calories', Integer())
    fat = Column('fat', REAL())
    fiber = Column('fiber', REAL())
    protein = Column('protein', REAL())
    category = Column('category', CHAR(20), nullable=False)
    image = Column('image', VARCHAR(400), default=None)
    title = Column('title', VARCHAR(200), nullable=False)
    createdAt = Column('created_at', TIMESTAMP())

    def __repr__(self):
        return f"<Food '{self.title}'>"
