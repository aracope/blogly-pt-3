"""Blogly application."""

from flask import Flask, redirect, render_template, request, redirect, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shh-this-is-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    """Show 5 most recent posts on homepage."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users/index.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def create_user():
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = request.form["image_url"] or None

    new_user = User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {first} {last} created successfully!", "success")
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} updated successfully!", "success")
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.get_full_name()} deleted successfully", "info")
    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{title}' created successfully!", "success")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    flash(f"Post '{post.title}' updated successfully!", "success")
    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    flash(f"Post “{post.title}” deleted successfully.", "info")
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("posts/list.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

