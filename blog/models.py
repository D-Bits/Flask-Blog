from blog import db
from datetime import datetime


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Profile pic
    profile_image_file_name = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # One-to-Many relationship to Post
    posts = db.relationship('Post', backref="author", lazy=True)

    # Define how objects are printed out
    def __repr__(self):

        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = username = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    # Define how objects are printed out
    def __repr__(self):

        return f"User('{self.title}', '{self.date_posted}')"