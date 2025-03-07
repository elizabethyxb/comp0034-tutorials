from flask import Blueprint
from flask import render_template

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/<string:name>')
def show_post(name):
    # show the post with the given id, the id is an integer
    return f'Hello {name}'