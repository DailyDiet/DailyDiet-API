import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    MONGO_URI = f'mongodb+srv://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@dailydiet-qeynf.mongodb.net/test?retryWrites=true&w=majority'


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_RESOURCES = {'*': {'origins': '*'}}


class ProductionConfig(Config):
    FLASK_DEBUG = False
    CORS_RESOURCES = {'https://daily-diet-aut.herokuapp.com/': {'origins': '*'}}


class TestingConfig(Config):
    TESTING = True
    FLASK_DEBUG = True
