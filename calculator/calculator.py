from flask import jsonify
from calculator.forms import BMIForm
from flask import Blueprint

calculator = Blueprint('calculator', __name__)


@calculator.route('/calculator/bmi', methods=['POST'])
def calculate_bmi():
    form = BMIForm()
    if form.validate_on_submit():
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
    else:
        return jsonify({"errors": form.errors}), 400
