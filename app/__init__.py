from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


# create instance of Flask
app = Flask(__name__, instance_relative_config=True)

#set config for app and sql database
app.config.from_object(Config)

# create an instance of SQLAlchemy called db
db = SQLAlchemy(app)

# need to import the routes to the application
from . import routes