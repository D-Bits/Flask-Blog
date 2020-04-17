from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from blog.forms import RegistrationForm, LoginForm
from blog import app, bcrypt, db
from blog.models import User


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

        # Hash AND salt the user's password w/ Bcrypt
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        # Add the new user to the db, and commit the transaction
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form, title="Register")


# Login existing users
@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash("Login failed. Please check username and/or password.", "danger")

    return render_template('login.html', form=form, title="Login")
