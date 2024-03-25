from flask import Flask 


app = Flask(__name__)

# need to import the routes to the application
from . import routes