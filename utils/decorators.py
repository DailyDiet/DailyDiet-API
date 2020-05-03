from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity

from users.models import User


def json_only(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        if not request.is_json:
            return {'error': 'Missing JSON in request.'}, 400
        return function(*args, **kwargs)
    return decorator


def confirmed_only(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.filter_by(Email=identity).first()
        if not user:
            return {'error': 'User not found.'}, 404
        if not user.Confirmed:
            return {'error': 'Your account is not activated.'}
        return function(*args, **kwargs)
    return decorator
