from foods import foods
from flask import jsonify, request
from foods.utils import get_foods_with_categories, set_placeholder, beautify_category
from foods.diet import sevade, yevade, dovade
from .models import Food
from flask_jwt_extended import (jwt_required)
from utils.decorators import confirmed_only


@foods.route('/yevade/<int:calorie>', methods=['GET'])
def get_yevade(calorie):
    if calorie > 0:
        cat = ['breakfast, ''mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers', 'drink']
        dog = get_foods_with_categories(cat)

        catdog = yevade(dog, calorie)

        if catdog is None:
            return jsonify({'error': 'Not Found'}), 404
        else:
            return jsonify({'diet': [str(catdog[0]), catdog[1]]}), 200
    else:
        return jsonify({'error': 'I\'m a teapot'}), 418


@foods.route('/dovade/<int:calorie>', methods=['GET'])
def get_dovade(calorie):
    if calorie > 0:
        cats1 = ['breakfast', 'sandwich', 'pasta', 'appetizers', 'drink']
        cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers']

        dogs1 = get_foods_with_categories(cats1)
        dogs2 = get_foods_with_categories(cats2)

        catdog = dovade(dogs1, dogs2, calorie)

        if catdog is None:
            return jsonify({'error': 'Not Found'}), 404
        else:
            return jsonify({'diet': [str(catdog[0]), str(catdog[1]), str(catdog[2])]}), 200
    else:
        return jsonify({'error': 'I\'m a teapot'}), 418


@foods.route('/sevade/<int:calorie>', methods=['GET'])
def get_sevade(calorie):
    if calorie > 0:
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
    else:
        return jsonify({'error': 'I\'m a teapot'}), 418


@foods.route('/recipe/<int:id>', methods=['GET'])
def get_recipe(id):
    food = Food.query.get(id)
    if food is None:
        return jsonify({"error": "food not found."}), 404

    recipe = food.recipe
    if recipe is None:
        return jsonify({"error": "recipe not found."}), 404

    if recipe['primary_image'] is None:
        recipe = set_placeholder(recipe)

    recipe['category'] = beautify_category(recipe['category'])
    return jsonify(recipe)


@foods.route('/<int:id>', methods=['GET'])
def get_food(id):
    food = Food.query.get(id)
    if food is None:
        return jsonify({"error": "food not found."}), 404

    payload = food.simple_view
    if payload['image'] is None:
        payload = set_placeholder(payload)
    return jsonify(payload)


@foods.route('/search', methods=['GET'])
def food_search():
    """
    food full text search using elasticsearch
    http parameters:
        query: text to search
        page: pagination page number
        per_page: pagination per_page count
    :return:
    """
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    if query == "" or query is None:
        return jsonify({
            'error': "query should exist in the request"
        }), 422  # invalid input error

    if per_page > 50:
        return jsonify({
            'error': 'per_page should not be more than 50'
        }), 422

    results, count = Food.search(query, page, per_page)

    return jsonify({
        'results': [set_placeholder(result.simple_view) for result in results.all()],
        'total_results_count': count
    })
