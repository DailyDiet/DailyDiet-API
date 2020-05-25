from extentions import db
from foods.models import Food

def get_foods_with_categories(categories):
    foods = []
    for cat in categories:
        foods +=  Food.query.filter_by(_Category=cat).all()
    return foods
