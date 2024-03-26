# Creating flask models here
# modesl of class CamelCase will automatically create tables snake_case

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # use db. to use SQLAlchemy types
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__set_password(kwargs.get('password', ''))
        
    def __repr__(self):
        return f"<User {self.id}|{self.username}>"


    # now automatically will add and commit to database when creating the user
    def save(self):
        db.session.add(self)
        db.session.commit()

     # hashes the password for security
    def __set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)
        self.save()

    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)

# u = User(first_name="Bob", last_name="Dylan", email="bd@rad.com", username="thebobdylan", password="123")