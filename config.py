import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_RESOURCES = {'*': {'origins': '*'}}


class TestingConfig(Config):
    TESTING = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    FLASK_DEBUG = False
    CORS_RESOURCES = {'https://daily-diet-aut.herokuapp.com/': {'origins': '*'}}


