# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    square_cust_id = db.Column(db.String(1000))

class Ad(db.Model):
    ad_id = db.Column(db.String(1000), primary_key=True) # primary keys are required by SQLAlchemy
    user_id = db.Column(db.String(1000))
    square_id = db.Column(db.String(1000))
