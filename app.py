from flask import Flask
from flask import request
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/lol")
def lol():
    return "<h1>Ala o cara programa em pythonkkkkkkkkkkkkkkkkk</h1>"


@app.route("/hello")
def hello():
    name = request.args.get("name", "Eddie")
    return f"Hello, {escape(name)}!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

from flask import render_template

@app.route('/index/<name>')
def index(name=None):
    return render_template('index.html', person=name)
    