from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from os import getenv
from dotenv import load_dotenv
from forms import RegistrationForm, LoginForm
from datetime import datetime


app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = getenv("SECRET_KEY")
# Set SQL Alchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Profile pic
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
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

posts = [
    {
        "author": "Dana",
        "title": "Post 1",
        "content": "First post.",
        "date_posted": "April 4th, 2020",
    },
    {
        "author": "Jim Lahey",
        "title": "Post 2",
        "content": "Have a drinky poo!",
        "date_posted": " April 2nd, 2020",
    }
]


# Load env vars from .env file
load_dotenv()

# Load environment type from environment var
ENV = getenv("ENV")

@app.route("/")
@app.route("/home")
def index():

    return render_template('index.html', title='Home', posts=posts)


@app.route("/about")
def about():
    
    return render_template('about.html', title='About')


# Register new users
@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        flash(f"Account created for {form.username.data}!", 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form, title="Register")


# Login existing users
@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        if form.email.data == "admin@blog.com" and form.password.data == "password":

            flash("You have been logged in.", "success")
            return redirect(url_for('index'))
        
        else:
            flash("Login failed. Please check username and/or password.", "danger")

    return render_template('login.html', form=form, title="Login")


if __name__ == '__main__':

    if ENV == 'dev':
        app.run(debug=True)
    else:
        pass