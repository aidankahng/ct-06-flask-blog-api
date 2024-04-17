from flask import request, render_template
from . import app, db
from .models import User, Post, Comment
from .auth import basic_auth, token_auth


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


@app.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    return user.get_token()


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
@token_auth.login_required
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

    current_user = token_auth.current_user()

    # Create a new Post instance with data and adding to db (hard coded user_id for now)
    new_post = Post(title=title, body=body, user_id=current_user.id)

    # Return the newly created Post as a dictionary with 201 status code
    return new_post.to_dict(), 201


# Update a post
@app.route('/posts/<int:post_id>', methods=["PUT"]) # PUT request to update
@token_auth.login_required
def edit_post(post_id):
    # check to see that they have a JSON body
    if not request.is_json:
        return {'error' : 'Your content-type must be application/json'}, 400
    # Now we need to find the post in the database
    post = db.session.get(Post, post_id) # will return None if no post exists
    if post is None:
        return {'error' : f'Post with an id #{post_id} does not exist'}, 404
    # verify that the person trying to make the change is the author
    # get the current user
    current_user = token_auth.current_user()
    if current_user is not post.author:
        return {'error' : f"This is not your post. You do not have permission to edit"}, 403
    # Able to edit, check their json and edit the post
    data = request.json
    post.update(**data) # use of **unpacks data into kwargs

    return post.to_dict()

# Delete Post
@app.route('/posts/<int:post_id>', methods=["DELETE"])
@token_auth.login_required
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        return {'error' : f"Post with an id #{post_id} does not exist"}, 404
    # Need to verify that the user trying to delete post is the one who created it
    current_user = token_auth.current_user()
    if current_user is not post.author:
        return {'error' : f"This is not your post. You do not have permission to delete"}, 403
    
    #delete the post
    post.delete()
    return {'success' : f"{post.title} was successfully deleted"}, 200

# Comment Endpoints

# Create a comment
@app.route('/posts/<int:post_id>/comments', methods=["POST"])
@token_auth.login_required
def create_comment(post_id):
    if not request.is_json:
        return {'error' : "Your content-type must be application/json"}, 400
    
    post = db.session.get(Post, post_id)
    if post is None:
        return {'error' : f'Post with an id #{post_id} does not exist'}, 404
    
    data = request.json

    required_fields = ["body"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    # If there are any missing fields, return 400 error with missing fields listed
    if missing_fields:
        return {'error' : f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    body = data.get('body')

    current_user = token_auth.current_user()

    new_comment = Comment(body=body, user_id=current_user.id, post_id=post.id)

    return new_comment.to_dict(), 201

# Delete a comment
@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=["DELETE"])
@token_auth.login_required
def delete_comment(post_id, comment_id):
    post = db.session.get(Post, post_id)
    comment = db.session.get(Comment, comment_id)
    if post is None or comment is None:
        return {'error' : f"Post #{post_id} or Comment #{comment_id} does not exist"}, 404
        
    current_user = token_auth.current_user()

    if comment.user is not current_user:
        return {"error" : "You do not have permission to delete this comment"}, 403
    
    if comment.post_id != post.id:
        return {'error' : f"Comment #{comment_id} is not associated with Post #{post_id}"}, 400
    
    #delete the post
    comment.delete()
    return {'success' : f"Comment #{comment.id} was successfully deleted"}, 200