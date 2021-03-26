"""Models for Blogly."""
import datetime
#import sql
from flask_sqlalchemy import SQLAlchemy


#execute sql alchemy
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String,
                        nullable=False)

    last_name = db.Column(db.String,
                        nullable=False)

    image_url = db.Column(db.String, default='No image')

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String, nullable=False)

    content = db.Column(db.Text,nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Format date"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
