from os import getenv

from flask import Flask

from calculator import calculator
from extentions import mongo


def create_app(environment='Development'):
    """
    :param environment: is either Development/Production/Testing
    """
    app = Flask(__name__)
    app.config.from_object(f'config.{environment}Config')
    app.register_blueprint(calculator)
    mongo.init_app(app)
    return app


if __name__ == '__main__':
    env = getenv('DAILYDIET_ENV')
    if env is None:
        create_app().run()
    else:
        create_app(env).run()
