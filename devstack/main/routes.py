from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
from devstack.models import Post

main = Blueprint('main', __name__)


# Home Route
@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('home.html', title='Home', posts=posts)
    else:
        return redirect(url_for('users.login'))


# About Route
@main.route('/about')
def about():
    return render_template('about.html', title='About')
