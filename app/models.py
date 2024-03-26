# Creating flask models here
# modesl of class CamelCase will automatically create tables snake_case

from . import db
from datetime import datetime

class User(db.Model):
    # use db. to use SQLAlchemy types
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


