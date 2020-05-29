from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    # database 
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_MAX_EMAILS = None

    # gmail authentication
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # admin settings

    # static file settings
    STATIC_FOLDERS = (
        'admin/static/',
        'static/'
    )

    # elasticsearch settings
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    CORS_RESOURCES = {'*': {'origins': '*'}}


class TestingConfig(Config):
    TESTING = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    FLASK_DEBUG = True
    CORS_RESOURCES = {'https://daily-diet-aut.herokuapp.com/': {'origins': '*'}}
