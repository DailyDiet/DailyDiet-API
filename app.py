from os import getenv

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from calculator import calculator
from users import users
from extentions import db

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

    db.init_app(app)
    migrate = Migrate(app, db)



    CORS(app, resources=app.config['CORS_RESOURCES'])
    return app


app = create_app(environment=getenv('DAILYDIET_ENV'))

if __name__ == '__main__':
    app.run()
