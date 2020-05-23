"""add extensions here"""
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()
migrate = Migrate(db=db)
jwt = JWTManager()
mail = Mail()

admin  = Admin(name='Dailydiet',template_mode='bootstrap3',url='/admin')
