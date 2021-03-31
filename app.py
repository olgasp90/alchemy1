"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post {new_post.title} added.")
    return redirect('/')

@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post_show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

################# Tags #############

@app.route('/tags')
def tags_idx():

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():

    posts = Post.query.all()

    return render_template('tags_form.html', posts=posts)

@app.route('/tags/new', methods=["POST"])
def new_tag():

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash('Your tag was added!')

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def tag_show(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag_edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tags(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    posts_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(posts_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash('Your tag has been successfully edited!')

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash('Your tag has been deleted!')

    return redirect('/tags')