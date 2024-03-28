# Creating flask models here
# models of class CamelCase will automatically create tables snake_case

import secrets
from . import db
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # use db. to use SQLAlchemy types
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(tz=timezone.utc))
    # Create a link to the posts table
    posts = db.relationship('Post', back_populates='author')
    # Create token and token expiration column, both allowed to be null or None
    token = db.Column(db.String, index=True, unique=True)
    token_expiration = db.Column(db.DateTime(timezone=True))

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
    
    def to_dict(self):
        return {
            "id" : self.id,
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "username" : self.username,
            "email" : self.email,
            "dateCreated" : self.date_created            
        }
    
    # Creates a new token or if one is valid returns current token
    def get_token(self):
        now = datetime.now(timezone.utc)
        if self.token and (self.token_expiration > now + timedelta(minutes=1)):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(hours=1)
        self.save()
        return {
            "token" : self.token,
            "tokenExpiration" : self.token_expiration
        }

# Example of creating a user:
# u = User(first_name="Bob", last_name="Dylan", email="bd@rad.com", username="thebobdylan", password="123")
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    # In PgSQL - user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCES user(id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Creates link to the user table 
    author = db.relationship('User', back_populates='posts')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.save()

    def __repr__(self) -> str:
        return f"<Post {self.id}|{self.title}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "body" : self.body,
            "dateCreated" : self.date_created,
            "author" : self.author.to_dict()
        }