import datetime

from sqlalchemy import Column, Integer, REAL, CHAR, VARCHAR, TIMESTAMP

from extentions import db


class Food(db.Model):
    __tablename__ = 'foods'

    id = Column('id', Integer(), primary_key=True)
    Calories = Column('calories', Integer())
    Fat = Column('fat', REAL())
    Fiber = Column('fiber', REAL())
    Protein = Column('protein', REAL())
    Category = Column('category', CHAR(20), nullable=False)
    Image = Column('image', VARCHAR(400), default=None)
    Title = Column('title', VARCHAR(200), nullable=False)
    CreatedAt = Column('created_at', TIMESTAMP())

    def __repr__(self):
        return f"<Food '{self.Title}'>"

    def __str__(self):
        return """{
            id:{id},
            calories:{calories},
            fat:{fat},
            fiber:{fiber},
            protein:{protein},
            category:{category},
            image:{image},
            title:{title}
        }""".format(id=self.id, calories=self.Calories, fat=self.Fat,
                    fiber=self.Fiber, protein=self.Protein, category=self.Category,
                    image=self.Image, title=self.Title)

    def get_calorie(self):
        return self.Calories
