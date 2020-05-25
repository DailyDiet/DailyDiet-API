from os import getenv
from werkzeug.debug import DebuggedApplication
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from calculator import calculator
from extentions import db, jwt, migrate, mail
from admin import admin
from users import users, models as user_models
from foods import foods, models as food_models


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
            'TESTING': app.config['TESTING']
        }

    app.register_blueprint(calculator)
    app.register_blueprint(users)
    app.register_blueprint(foods)

    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    @app.route('/admin/static/<path:path>')
    def handle_admin_files(path):
        """
        temp function to load static files from admin/static folder
        todo:move it to a general blueprint that doe'nt have prefix
        :param path:
        :return:
        """
        return send_from_directory('admin/static', path)

    # configuring CORS settings
    CORS(app, resources=app.config['CORS_RESOURCES'])

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app


app = create_app(environment=getenv('DAILYDIET_ENV'))

if __name__ == '__main__':
    app.run()
