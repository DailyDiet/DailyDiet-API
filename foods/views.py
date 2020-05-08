from foods import foods
from foods.utils import get_foods_with_categories
from foods.diet import sevade

@foods.route('/sevade/<calorie>', methods=['GET'])
def get_sevade(calorie):
    cats1 = ['breakfast']
    cats2 = ['mostly_meat', 'pasta', 'main_dish', 'sandwich']
    cats3 = ['dessert', 'other', 'salad']

    dogs1 = get_foods_with_categories(cats1)
    dogs2 = get_foods_with_categories(cats2)
    dogs3 = get_foods_with_categories(cats3)

    catdog = sevade(dogs1, dogs2, dogs3, calorie)

    if catdog is None:
        return {'error': 'Not Found'}, 404
    else:
        return {'diet': [str(catdog[0]), str(catdog[1]), str(catdog[2]), catdog[3]]}, 200
