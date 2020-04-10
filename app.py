from flask import Flask
from os import getenv
from extentions import mongo
from calculator.calculator import calculator


def create_app(environment='Development'):
    """
    :param environment: is either Development/Production/Testing
    """
    if environment is None:
        environment = 'Development'
    app = Flask(__name__)
    app.config.from_object(f'config.{environment}Config')
    app.register_blueprint(calculator)
    mongo.init_app(app)
    return app


app = create_app(environment=getenv('DAILYDIET_ENV'))

if __name__ == '__main__':
    app.run()
