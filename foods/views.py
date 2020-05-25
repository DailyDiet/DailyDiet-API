from foods import foods
from flask import jsonify
from foods.utils import get_foods_with_categories
from foods.diet import sevade, yevade, dovade
from .models import Food
from flask_jwt_extended import (jwt_required)
from utils.decorators import confirmed_only

@foods.route('/yevade/<int:calorie>', methods=['GET'])
def get_yevade(calorie):
    cat = ['breakfast, ''mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers', 'drink']
    dog = get_foods_with_categories(cat)

    catdog = yevade(dog, calorie)

    if catdog is None:
        return jsonify({'error': 'Not Found'}), 404
    else:
        return jsonify({'diet': [str(catdog[0]), catdog[1]]}), 200


@foods.route('/dovade/<int:calorie>', methods=['GET'])
def get_dovade(calorie):
    cats1 = ['breakfast', 'sandwich', 'pasta', 'appetizers', 'drink']
    cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers']

    dogs1 = get_foods_with_categories(cats1)
    dogs2 = get_foods_with_categories(cats2)

    catdog = dovade(dogs1, dogs2, calorie)

    if catdog is None:
        return jsonify({'error': 'Not Found'}), 404
    else:
        return jsonify({'diet': [str(catdog[0]), str(catdog[1]), str(catdog[2])]}), 200


@foods.route('/sevade/<int:calorie>', methods=['GET'])
def get_sevade(calorie):
    cats1 = ['breakfast', 'pasta', 'salad', 'sandwich', 'appetizers']
    cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich']
    cats3 = ['dessert', 'other', 'salad', 'side_dish', 'drink', 'main_dish', 'pasta']

    dogs1 = get_foods_with_categories(cats1)
    dogs2 = get_foods_with_categories(cats2)
    dogs3 = get_foods_with_categories(cats3)

    catdog = sevade(dogs1, dogs2, dogs3, calorie)

    if catdog is None:
        return jsonify({'error': 'Not Found'}), 404
    else:
        return jsonify({'diet': [str(catdog[0]), str(catdog[1]), str(catdog[2]), catdog[3]]}), 200


@foods.route('/recipe/<int:id>', methods=['GET'])
def get_recipe(id):
    food = Food.query.get(id)
    if food is None:
        return jsonify({"error": "food not found."}), 404

    recipe = food.recipe
    if recipe is None:
        return jsonify({"error": "recipe not found."}), 404

    return jsonify(recipe)


@foods.route('/<int:id>', methods=['GET'])
def get_food(id):
    food = Food.query.get(id)
    if food is None:
        return jsonify({"error": "food not found."}), 404

    return jsonify(food.simple_view)
