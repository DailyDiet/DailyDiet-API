"""add extensions here"""
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from config import Config

db = SQLAlchemy()
migrate = Migrate(db=db)
jwt = JWTManager()
mail = Mail()
elastic = Elasticsearch(Config.ELASTICSEARCH_URL) if Config.ELASTICSEARCH_URL else None
