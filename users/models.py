import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from extentions import db


class User(db.Model):

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    FullName = Column(String(), unique=False, nullable=False)
    Email = Column(String(), unique=True, nullable=False)
    Password = Column(String(), nullable=False)
    Admin = Column(Boolean(), nullable=False, default=False)
    RegisteredOn = Column(DateTime(), nullable=False)
    Confirmed = Column(Boolean(), nullable=False, default=False)    # Confirmed Email Address Or Not
    ConfirmedOn = Column(DateTime(), nullable=True)

    def __init__(self, full_name, email, password, admin=False,
                 registerd_on=None, confirmed=False, confirmed_on=None):

        self.FullName = full_name
        self.Email = email
        self.Password = generate_password_hash(password)
        self.Admin = admin
        self.RegisteredOn = registerd_on or datetime.datetime.now()
        self.Confirmed = confirmed
        self.ConfirmedOn = confirmed_on

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def __repr__(self):
        return f'<Email {self.Email}>'
