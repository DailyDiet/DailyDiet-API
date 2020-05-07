from flask import Blueprint


foods = Blueprint('users', __name__, url_prefix='/food/')


from foods import views