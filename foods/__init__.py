from flask import Blueprint


foods = Blueprint('foods', __name__, url_prefix='/foods/')


from foods import views
