from flask import Blueprint


calculator = Blueprint('calculator', __name__, url_prefix='/calculate/')


from calculator import views
