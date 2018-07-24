from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from devstack import db
from devstack.models import Post, User
from devstack.posts.forms import PostForm

posts = Blueprint('posts', __name__)


# New Post Route
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form,
                           legend='New Post')


# Post Route
@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# Update Post Route
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post')


# Delete Post Route
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('main.home'))


# User Posts Route
@posts.route('/user/<string:username>')
def user_post(username):
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
        return render_template('user_post.html', title='Home', posts=posts, user=user)
    else:
        return redirect(url_for('users.login'))
