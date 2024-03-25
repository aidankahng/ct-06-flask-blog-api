#import the Flask class from flack module
from flask import Flask 

# create instance of Flask called app. primary object
app = Flask(__name__)

#Define a route (to a specific url)
@app.route("/")
def hello_world():
    first = "John"
    return f"Hello there {first}!"

@app.route("/test")
def test():
    my_dicts = []
    for i in range(5):
        a_dict = {
            'id' : i+1,
            'square' : i**2
        }
        my_dicts.append(a_dict)

    return my_dicts


## In terminal to run
## flask --app app run -p 5050
## if name is app.py:
## flask run

## Tu run debug mode:
## add --debug