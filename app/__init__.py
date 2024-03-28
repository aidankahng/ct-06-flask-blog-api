# base flask
from flask import Flask
# sql-alchemy support for flask
from flask_sqlalchemy import SQLAlchemy
# flask-igrate uses alembic to work with databases
from flask_migrate import Migrate
# Gets the Config from our locat config.py file/module
from config import Config


# create instance of Flask
app = Flask(__name__, instance_relative_config=True)

#set config for app and sql database
app.config.from_object(Config)

# create an instance of SQLAlchemy called db
db = SQLAlchemy(app)

#create an instance of Migrate with the app and db
migrate = Migrate(app, db)

# need to import the routes to the application
# also import the models to the application
from . import routes, models