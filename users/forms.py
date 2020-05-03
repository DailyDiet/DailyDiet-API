from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from users.models import User


class RegisterForm(FlaskForm):
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


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    class Meta:
        csrf = False

    old_password = PasswordField('old password', validators=[DataRequired(), Length(min=6, max=25)])
    new_password = PasswordField('new password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField('repeat password', validators=[DataRequired(), EqualTo('new_password', message='passwords must match')])
