from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class BMIForm(FlaskForm):
    class Meta:
        csrf = False

    height = IntegerField('height', validators=[DataRequired(), NumberRange(50, 210)])  # height in centimeter
    weight = DecimalField('weight', validators=[DataRequired(), NumberRange(20, 150)])  # weight in kilograms
