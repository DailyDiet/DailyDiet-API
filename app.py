from os import getenv

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.debug import DebuggedApplication
from whitenoise import WhiteNoise

from admin import admin
from blog import blog
from calculator import calculator
from extentions import db, elastic, jwt, mail, migrate
from foods import foods
from foods import models as food_models
from users import models as user_models
from users import users


def create_app(environment='Development'):
    """
    :param environment: is either Development/Production/Testing
    """
    if environment is None:
        environment = 'Development'

    app = Flask(__name__)

    app.config.from_object(f'config.{environment}Config')

    @app.route('/', methods=['GET'])
    def temp_main_function():
        """
        temporary main function to test app, debug and testing status
        todo:move it to another endpoint
        :return: status:dict
        """
        return {
            'status': 'API is up and running:))',
            'ENV': app.config['ENV'],
            'DEBUG': app.config['DEBUG'],
            'TESTING': app.config['TESTING'],
            'elasticsearch_status': 'ready' if elastic.ping() else 'broken'
        }

    app.register_blueprint(calculator)
    app.register_blueprint(blog)
    app.register_blueprint(users)
    app.register_blueprint(foods)


    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    # configuring CORS settings
    CORS(app, resources=app.config['CORS_RESOURCES'])

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    # enabling whitenoise
    app.wsgi_app = WhiteNoise(app.wsgi_app)
    for static_folder in app.config['STATIC_FOLDERS']:
        app.wsgi_app.add_files(static_folder)

    return app


app = create_app(environment=getenv('DAILYDIET_ENV'))

if __name__ == '__main__':
    app.run()
