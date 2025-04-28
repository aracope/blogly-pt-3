"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app."""
    db.app = app
    db.init_app(app)

def __repr__(self):
    return f"<Tag id={self.id} name={self.name}>"

class User(db.Model):
    """User model for Blogly"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(
        db.String,
        nullable=False,
        default="https://cdn-icons-png.flaticon.com/512/149/149071.png"
    )

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} name={self.first_name} {self.last_name}>"
    
    def get_full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship('Tag', secondary='posts_tags', back_populates='posts')

    def __repr__(self):
        return f"<Post id={self.id} title={self.title} created_at={self.created_at}>"

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    posts = db.relationship('Post', secondary='posts_tags', back_populates='tags')



class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)




