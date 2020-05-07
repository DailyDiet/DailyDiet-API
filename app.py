from os import getenv

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from calculator import calculator
from extentions import db, jwt, migrate, mail
from users import users
from foods import foods


def create_app(environment='Development'):
    """
    :param environment: is either Development/Production/Testing
    """
    if environment is None:
        environment = 'Development'
        
    app = Flask(__name__)

    app.config.from_object(f'config.{environment}Config')

    app.register_blueprint(calculator)
    app.register_blueprint(users)
    app.register_blueprint(foods)

    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    CORS(app, resources=app.config['CORS_RESOURCES'])
    
    return app


app = create_app(environment=getenv('DAILYDIET_ENV'))

if __name__ == '__main__':
    app.run()
