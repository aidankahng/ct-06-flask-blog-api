from app import app

@app.route("/")
def hello_world():
    first = "John"
    return f"Hello there {first}!"

@app.route("/test")
def test():
    my_dicts = []
    for i in range(1,10):
        a_dict = {
            'id' : i,
            'square' : i**2,
            'cube' : i**3
        }
        my_dicts.append(a_dict)

    return my_dicts