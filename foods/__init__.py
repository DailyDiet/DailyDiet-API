from flask import Blueprint


foods = Blueprint('foods', __name__, url_prefix='/food/')


from foods import views
