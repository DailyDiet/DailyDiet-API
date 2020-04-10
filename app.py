from flask import Flask
from os import getenv
from extentions import mongo
from calculator.calculator import calculator


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
        app = create_app()
    else:
        app = create_app(env)

    app.run()
