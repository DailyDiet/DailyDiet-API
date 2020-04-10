from random import randrange

from flask import jsonify

from calculator import calculator
from calculator.forms import BMIForm, CalorieForm


@calculator.route('/bmi', methods=['POST'])
def calculate_bmi():
    form = BMIForm()
    if not form.validate_on_submit():
        return jsonify({"errors": form.errors}), 400

    height_in_meters = form.height.data / 100
    bmi_value = float(form.weight.data) / (height_in_meters ** 2)
    bmi_status = None
    if bmi_value < 18.5:
        bmi_status = 'Underweight'
    elif bmi_value < 25:
        bmi_status = 'Normal weight'
    elif bmi_value < 30:
        bmi_status = 'Overweight'
    else:
        bmi_status = 'Obesity'

    result = {
        "bmi_value": round(bmi_value, 2),
        "bmi_status": bmi_status
    }
    return jsonify(result)


@calculator.route('/calorie', methods=['POST'])
def calculate_calorie():
    form = CalorieForm()
    if not form.validate_on_submit():
        return jsonify({"errors": form.errors}), 400

    bmr = None
    if form.gender.data == 'male':
        bmr = 66 + (13.7 * float(form.weight.data)) + (5 * form.height.data) - (6.8 * form.age.data)
    elif form.gender.data == 'female':
        bmr = 655 + (9.6 * float(form.weight.data)) + (1.8 * form.height.data) - (4.7 * form.age.data)

    calorie = None
    activity = form.activity.data
    if activity == 'sedentary':
        calorie = bmr * 1.2
    elif activity == 'lightly':
        calorie = bmr * 1.375
    elif activity == 'moderately':
        calorie = bmr * 1.55
    elif activity == 'very':
        calorie = bmr * 1.725
    elif activity == 'extra':
        calorie = bmr * 1.9

    goal = form.goal.data
    if goal == 'lose_weight':
        calorie = calorie - randrange(500, 750)
    elif goal == 'build_muscle':
        calorie = calorie + randrange(500, 750)
    elif goal == 'maintain':
        pass

    result = {
        "calorie": int(calorie)
    }

    return jsonify(result)
