from flaskblog import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from dataclasses import dataclass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@dataclass
class User(db.Model, UserMixin):
    id:int
    username:str
    facebook:str
    twitter:str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    facebook = db.Column(db.String(30), nullable=False, default='You haven\'t set your facebook adress ')
    twitter = db.Column(db.String(30), nullable=False, default='You haven\'t set your twitter adress ')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='commenter', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}','{self.image_file}')"

@dataclass
class Post(db.Model):
    id:int
    title:str
    category:str
    author_username:str
    content:str

    def get_time():
        return (datetime.utcnow() + timedelta(hours=3))
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=get_time)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_username = db.Column(db.Text, nullable=False)

    comments = db.relationship('Comment', backref='commented_post', lazy='dynamic')


    def __repr__(self):
        return f"Post('{self.title}', '{self.author.username}', '{self.date_posted}')"

@dataclass
class Comment(db.Model):

    def get_time():
        return (datetime.utcnow() + timedelta(hours=3))

    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=get_time)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Comment('{self.id}', '{self.content}', '{self.date_posted}', '{self.commenter.username}')"
