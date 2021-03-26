"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly_password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404


########## User ##########
@app.route('/users')
def users_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    new = User(
        first_name=request.form['first'],
        last_name=request.form['last'],
        image_url=request.form['image'] or None
    )
    db.session.add(new)
    db.session.commit()
    flash(f"User {new.first_name} added")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_users(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()
    flash(f'User {user.first_name} {user.last_name} edited.')

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.first_name} {user.last_name} deleted.')

    return redirect('/users')


######### Posts ##########
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    post = Post(title=request.form['title'], content=request.form['content'], user=user)

    db.session.add(post)
    db.session.commit()
    flash(f"Post {post.title} added.")
    return redirect('/')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash('Your changes were saved!')

    return redirect('/')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted successfully!')

    return  redirect('/')
