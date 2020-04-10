from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, FloatField
from wtforms.validators import AnyOf, DataRequired, NumberRange


class BMIForm(FlaskForm):
    class Meta:
        csrf = False

    height = IntegerField('Height', validators=[DataRequired(), NumberRange(50, 210)])  # height in centimeter
    weight = DecimalField('Weight', validators=[DataRequired(), NumberRange(20, 150)])  # weight in kilograms


class CalorieForm(FlaskForm):
    class Meta:
        csrf = False
    
    goal = StringField('Goal', validators=[DataRequired(), AnyOf(['lose_weight', 'maintain', 'build_muscle'])])
    gender = StringField('Gender', validators=[DataRequired(), AnyOf(['male', 'female'])]) 
    height = IntegerField('Height', validators=[DataRequired(), NumberRange(50, 210)])  # height in centimeter
    weight = DecimalField('Weight', validators=[DataRequired(), NumberRange(20, 150)])  # weight in kilograms
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(1, 120)])         # age in years
    activity = StringField('Activity Level', validators=[DataRequired(), AnyOf(['sedentary', 'lightly', 'moderately', 'very', 'extra'])])
