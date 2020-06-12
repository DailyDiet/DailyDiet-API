from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import Config
from foods import foods
from foods.diet import dovade, sevade, yevade
from foods.utils import (beautify_category, get_foods_with_categories,
                         set_placeholder)
from utils.decorators import confirmed_only
from users.models import User

from .models import Food, DietRecord, SearchTimedOutException
from extentions import db


def submit_diet_record(food_ids, jwt_identity):
    user = User.query.filter_by(Email=jwt_identity).first()
    if user is None:
        return
    diet_record = DietRecord(ownerId=user.id, diet=food_ids)
    db.session.add(diet_record)
    db.session.commit()


@foods.route('/yevade/<int:calorie>', methods=['GET'])
@jwt_required
def get_yevade(calorie):
    if calorie > 0:
        cat = ['breakfast', 'mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers', 'drink']
        dog = get_foods_with_categories(cat)

        catdog = yevade(dog, calorie)

        if catdog is None:
            return jsonify({'error': 'Not Found'}), 404
        else:
            submit_diet_record([catdog[0].id], get_jwt_identity())
            return jsonify({'diet': [catdog[0].simple_view, catdog[1]]}), 200
    else:
        return jsonify({'error': 'Calorie value can\'t be zero'}), 418


@foods.route('/dovade/<int:calorie>', methods=['GET'])
@jwt_required
def get_dovade(calorie):
    if calorie > 0:
        cats1 = ['breakfast', 'sandwich', 'pasta', 'appetizers', 'drink', 'mostly_meat', 'appetizers', 'mostly_meat']
        cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich', 'appetizers', 'breakfast', 'drink']

        dogs1 = get_foods_with_categories(cats1)
        dogs2 = get_foods_with_categories(cats2)

        catdog = dovade(dogs1, dogs2, calorie)

        if catdog is None:
            return jsonify({'error': 'Not Found'}), 404
        else:
            submit_diet_record([catdog[0].id, catdog[1].id], get_jwt_identity())
            return jsonify({'diet': [catdog[0].simple_view, catdog[1].simple_view, catdog[2]]}), 200
    else:
        return jsonify({'error': 'Calorie value can\'t be zero'}), 418


@foods.route('/sevade/<int:calorie>', methods=['GET'])
@jwt_required
def get_sevade(calorie):
    if calorie > 0:
        cats1 = ['breakfast', 'pasta', 'salad', 'sandwich', 'appetizers', 'drink']
        cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich', 'breakfast', 'drink', 'salad', 'breakfast']
        cats3 = ['dessert', 'other', 'salad', 'side_dish', 'drink', 'main_dish', 'pasta', 'breakfast']

        dogs1 = get_foods_with_categories(cats1)
        dogs2 = get_foods_with_categories(cats2)
        dogs3 = get_foods_with_categories(cats3)

        catdog = sevade(dogs1, dogs2, dogs3, calorie)

        if catdog is None:
            return jsonify({'error': 'Not Found'}), 404
        else:
            submit_diet_record([catdog[0].id, catdog[1].id, catdog[2].id], get_jwt_identity())
            return jsonify(
                {'diet': [catdog[0].simple_view, catdog[1].simple_view, catdog[2].simple_view, catdog[3]]}), 200
    else:
        return jsonify({'error': 'Calorie value can\'t be zero'}), 418


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

    try:
        results, count = Food.search(query, page, per_page)
    except SearchTimedOutException as e:
        return jsonify({
            "error": "search request timed out."
        }), 408

    return jsonify({
        'results': [set_placeholder(result.simple_view) for result in results.all()],
        'total_results_count': count
    })


@foods.route('/search', methods=['POST'])
def food_advanced_search():
    """
    advanced + full text search using elasticsearch
    http post content json parameters:
        query: query to search with below format
        {
            "text": text_to_search | null | "",
            "category" : cat (one of 13 categories),
            "ingredients": [list of ingredient ids]
            "calories, carbs , fats ,proteins , cook_time ,prep_time , total_time, :{
                "min":optional,
                "max":optional
            },
            "page": pagination page number
            "per_page": pagination per_page count
        }

    :return:
    """
    input_json = request.get_json()
    page = 1 if input_json.get('page') is None else input_json['page']
    per_page = 10 if input_json.get('per_page') is None else input_json['per_page']

    # if query == "" or query is None:
    #     return jsonify({
    #         'error': "query should exist in the request"
    #     }), 422  # invalid input error

    if per_page > 50:
        return jsonify({
            'error': 'per_page should not be more than 50'
        }), 422

    try:
        results, count = Food.advanced_search(input_json)
    except SearchTimedOutException as e:
        return jsonify({
            "error": "search request timed out."
        }), 408

    return jsonify({
        'results': [set_placeholder(result.simple_view) for result in results.all()],
        'total_results_count': count
    })


@foods.route('/search/ingredient', methods=['GET'])
def ingredient_search():
    """
    ingredient full text search using elasticsearch
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

    try:
        results, count = Food.ingredient_search(query, page, per_page)
    except SearchTimedOutException as e:
        return jsonify({
            "error": "search request timed out."
        }), 408

    # setting placeholder
    for result in results:
        if result['primary_thumbnail'] is None:
            result['primary_thumbnail'] = Config.PLACEHOLDERS['thumbnail']['ingredient']

    return jsonify({
        'results': results,
        'total_results_count': count
    })


@jwt_required
@foods.route('/diets', methods=['GET'])
def get_diet_records():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    user = User.query.filter_by(Email=get_jwt_identity()).first()
    if user is None:
        return {
                   "error": "user not found"
               }, 404
    results = DietRecord.query.filter(DietRecord.ownerId == user.id).order_by('generated_at desc') \
        .limit(per_page) \
        .offset((page - 1) * per_page).all()

    payload = []
    for diet_record in results:
        payload.append({
            "diet": [Food.query.get_or_404(food_id).simple_view for food_id in diet_record.diet],
            "time": diet_record.generatedAt
        })

    return payload
