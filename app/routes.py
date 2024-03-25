from flask import request
from app import app
from fake_data.posts import post_data



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


@app.route('/posts')
def get_posts():
    posts = post_data
    return posts


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    print(post_id, type(post_id))
    # get the post from fake post_data
    posts = post_data
    for post in posts:
        if post['id'] == post_id:
            return post
    # If we loop through and can't find any such post we get an error:
    return {'error': f"Post with an ID of {post_id} does not exist"}, 404


@app.route('/posts', methods=['POST'])
def create_posts():
    # Check if the request body is JSON
    if not request.is_json:
        return {'error' : "Your content-type must be application/json"}, 400
    # If JSON, get the data from request body
    data = request.json
    required_fields = ["title", "body"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    # If there are any missing fields, return 400 error with missing fields listed
    if missing_fields:
        return {'error' : f"{', '.join(missing_fields)} must be in the request body"}, 400

    # Get data values
    title = data.get('title')
    body = data.get('body')

    # Create a new post dictionary with the data
    new_post = {
        "id" : len(post_data) + 1,
        "title" : title,
        "body" : body,
        "userId" : 1,
        "dateCreated" : "2024-03-25T15:31:25",
        "likes" : 0
    }

    # Add the new post to storage (post_data, will be a database later)
    post_data.append(new_post)

    # Return the newly created post dictionary with 201 status code
    return new_post, 201
