from flask_wtf import Form
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from users.models import User


class RegisterForm(Form):
    class Meta:
        csrf = False

    full_name = TextField('full name', validators=[DataRequired(), Length(max=70)])
    email = TextField('email', validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField( 'password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(Email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered.")
            return False
        return True


class LoginForm(Form):
    class Meta:
        csrf = False

    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class ChangePasswordForm(Form):
    class Meta:
        csrf = False

    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
