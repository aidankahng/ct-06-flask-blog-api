#import the Flask class from flack module
from flask import Flask 

# create instance of Flask called app. primary object
app = Flask(__name__)

#Define a route (to a specific url)
@app.route("/")
def hello_world():
    first = "John"
    return f"Hello there {first}!"

## In terminal to run
## flask --app hello run -p 5050
## if name is app.py:
## flask run

## Tu run debug mode:
## add --debug