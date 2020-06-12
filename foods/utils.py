from extentions import db
from foods.models import Food
from config import Config


def get_foods_with_categories(categories):
    foods = []
    for cat in categories:
        foods += Food.query.filter_by(Category=cat).all()
    return foods


def set_placeholder(recipe):
    category = recipe['category']

    if 'images' in recipe:
        # its a recipe dict
        recipe['images'].append({
            "id": 0,
            "image": Config.PLACEHOLDERS['image'][category],
            "thumbnail": Config.PLACEHOLDERS['thumbnail'][category]
        })
        if recipe['primary_image'] is None:
            recipe['primary_image'] = Config.PLACEHOLDERS['image'][category]
            recipe['primary_thumbnail'] = Config.PLACEHOLDERS['thumbnail'][category]
    else:
        # its a small view dict
        if recipe['image'] is None:
            recipe['image'] = Config.PLACEHOLDERS['image'][category]
            recipe['thumbnail'] = Config.PLACEHOLDERS['thumbnail'][category]

    return recipe


def beautify_category(category: str):
    return category.replace('_', ' ').lower()


def uglify_category(category: str):
    return category.replace(' ', '_').lower()
