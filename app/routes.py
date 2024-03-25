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

    