from flask import Flask 


app = Flask(__name__, instance_relative_config=True)

# need to import the routes to the application
from . import routes