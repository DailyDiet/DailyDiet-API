import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from extentions import db


class User(db.Model):

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    registered_on = Column(DateTime(), nullable=False)
    admin = Column(Boolean(), nullable=False, default=False)
    confirmed = Column(Boolean(), nullable=False, default=False)
    confirmed_on = Column(DateTime(), nullable=True)

    def __init__(self, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'<email {self.email}>'
