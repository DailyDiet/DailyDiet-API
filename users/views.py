import datetime

from flask import jsonify, render_template, request, url_for
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_refresh_token_required,
                                jwt_required)

from extentions import db
from users import users
from users.email import send_email
from users.forms import ChangePasswordForm, LoginForm, RegisterForm
from users.models import User
from users.token import confirm_token, generate_confirmation_token
from utils.decorators import confirmed_only, json_only


@users.route('/signup', methods=['POST'])
def create_user():
    form = RegisterForm()
    if not form.validate_on_submit():
        return {'errors': form.errors}, 400
    new_user = User(form.full_name.data, form.email.data, form.password.data)
    db.session.add(new_user)
    db.session.commit()
    token = generate_confirmation_token(new_user.Email)
    subject = 'DailyDiet | Email Confirmation'
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = html = render_template('users/activate.html', confirm_url=confirm_url)
    send_email(new_user.Email, subject, html)
    return {'msg': 'Account created successfully!'}, 201


@users.route('/signup/confirmation/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return {'error': 'The confirmation link is invalid or has expired.'}, 400
    user = User.query.filter_by(Email=email).first()
    if not user:
        return {'error': 'User not found.'}, 404
    if user.Confirmed:
        return {'error': 'Account already confirmed. Please login.'}, 400
    else:
        user.Confirmed = True
        user.ConfirmedOn = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return {}, 204


@users.route('/signin', methods=['POST'])
def login():
    form = LoginForm()
    if not form.validate_on_submit():
        return {'errors': form.errors}, 400
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(Email=email).first()
    if not user:
        return {'error': 'Email or Password does not match.'}, 403
    if not user.check_password(password):
        return {'error': 'Email or Password does not match.'}, 403
    access_token = create_access_token(identity=user.Email, fresh=True)
    refresh_token = create_refresh_token(identity=user.Email)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@users.route('/auth', methods=['PUT'])
@jwt_refresh_token_required
def get_new_access_token():
    identity = get_jwt_identity()
    return {'access_token': f'{create_access_token(identity=identity)}'}, 200


@users.route('/signup/resendConfrimation', methods=['GET'])
@jwt_required
def resend_confirmation():
    identity = get_jwt_identity()
    token = generate_confirmation_token(identity)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/activate.html', confirm_url=confirm_url)
    subject = 'DailyDiet | Email Confirmation'
    send_email(identity, subject, html)
    return {'msg': 'A new confirmation email has been sent.'}, 200


@users.route('/signup/modify', methods=['PATCH'])
@jwt_required
def change_password():
    identity = get_jwt_identity()
    user = User.query.filter_by(Email=identity).first()
    form = ChangePasswordForm()
    if not user.check_password(form.old_password.data):
        return {'error': 'Old password does not match.'}, 403
    if not form.validate_on_submit():
        return {'errors': form.errors}, 400
    user.set_password(form.new_password.data)
    db.session.commit()
    return {}, 204


@users.route('/signout', methods=['PATCH'])
def log_out():
    identity = get_jwt_identity()
    user = User.query.filter_by(Email=identity).first()
    return {}, 204


@users.route('/get_user', methods=['GET'])
@jwt_required
def get_user():
    identity = get_jwt_identity()
    user = User.query.filter_by(Email=identity).first()
    return {'full_name': f'{user.FullName}', 
            'email': f'{user.Email}',
            'confirmed': f'{user.Confirmed}'}
  