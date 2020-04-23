import datetime

from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required,
                                jwt_required)
from sqlalchemy.exc import IntegrityError

from extentions import db
from users import users
from users.forms import ChangePasswordForm, LoginForm, RegisterForm
from users.models import User


@users.route('/register', methods=['POST'])
def create_user():
    form = RegisterForm()
    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    new_user = User(form.full_name.data, form.email.data, form.password.data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully.'}), 201
