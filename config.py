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

    PLACEHOLDERS = {
        "image": {
            "mostly_meat": "https://img.icons8.com/color/7x/steak.png",
            "appetizers": "https://img.icons8.com/color/7x/nachos.png",
            "drink": "https://img.icons8.com/color/7x/rice-vinegar.png",
            "main_dish": "https://img.icons8.com/color/7x/real-food-for-meals.png",
            "sandwich": "https://img.icons8.com/color/7x/sandwich.png",
            "dessert": "https://img.icons8.com/color/7x/dessert.png",
            "breakfast": "https://img.icons8.com/color/7x/breakfast.png",
            "protein_shake": "https://img.icons8.com/color/7x/protein.png",
            "salad": "https://img.icons8.com/color/7x/salad.png",
            "pasta": "https://img.icons8.com/color/7x/spaghetti.png",
            "other": "https://img.icons8.com/color/7x/cookbook.png",
            "ingredient": "https://img.icons8.com/color/7x/grocery-bag.png"
        },
        "thumbnail": {
            "mostly_meat": "https://img.icons8.com/color/2x/steak.png",
            "appetizers": "https://img.icons8.com/color/2x/nachos.png",
            "drink": "https://img.icons8.com/color/2x/rice-vinegar.png",
            "main_dish": "https://img.icons8.com/color/2x/real-food-for-meals.png",
            "sandwich": "https://img.icons8.com/color/2x/sandwich.png",
            "dessert": "https://img.icons8.com/color/2x/dessert.png",
            "breakfast": "https://img.icons8.com/color/2x/breakfast.png",
            "protein_shake": "https://img.icons8.com/color/2x/protein.png",
            "salad": "https://img.icons8.com/color/2x/salad.png",
            "pasta": "https://img.icons8.com/color/2x/spaghetti.png",
            "other": "https://img.icons8.com/color/2x/cookbook.png",
            "ingredient":"https://img.icons8.com/color/2x/grocery-bag.png"
        }
    }


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    CORS_RESOURCES = {'*': {'origins': '*'}}


class TestingConfig(Config):
    TESTING = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    FLASK_DEBUG = True
    CORS_RESOURCES = {'https://daily-diet-aut.herokuapp.com/': {'origins': '*'}}
