from flask import request, render_template
from . import app, db
from .models import User, Post


@app.route("/")
def index():
    return render_template("index.html")


# User Endpoints

# Create new user endpoint
@app.route("/users", methods=["POST"])
def create_user():
    # check to make sure that the request is JSON
    if not request.is_json:
        return {"error" : "Your content type must be application/JSON"}, 400
    # get the data from the request body
    data = request.json

    # Validate that the data has all the required fields
    required_fields = ["firstName", "lastName", "username", "email", "password"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {"error" : f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Pull the individual data from the body
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check to see if any current users already have that username or email
    # db.session.get(User, 6) <-- will retrieve user with id of 6
    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    # Executing a SELECT * FROM user WHERE username = username OR email = email;
    if check_users:
        return {'error' : "A user with that username and/or email already exists"}, 400
    
    # Create a new instance of user with the data from the request
    new_user = User(first_name=first_name, last_name=last_name,  username=username, email=email, password=password)

    # Convert User object to a dictionary to display
    return new_user.to_dict(), 201


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

# Get all posts / search for title match
@app.route('/posts')
def get_posts():
    search = request.args.get('search')
    select_stmt = db.select(Post)
    if search:
        select_stmt = select_stmt.where(Post.title.ilike('%' + search + '%'))
    # Get the posts from the database
    posts = db.session.execute(select_stmt).scalars().all()
    # return a list of dictionaries 
    return [p.to_dict() for p in posts], 200

# Get single post by id
@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # Get either a Post of post_id or None
    post = db.session.get(Post, post_id)
    if post: 
        return post.to_dict()
    # If we loop through and can't find any such post we get an error:
    return {'error': f"Post with an ID of {post_id} does not exist"}, 404

# Create a post
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

    # Create a new Post instance with data and adding to db (hard coded user_id for now)
    new_post = Post(title=title, body=body, user_id=2)

    # Return the newly created Post as a dictionary with 201 status code
    return new_post.to_dict(), 201
