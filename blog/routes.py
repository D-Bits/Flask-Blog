from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegistrationForm, LoginForm, UpdateAccountInfo
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
@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


# Logout users that are currently logged in
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('index'))


# Route for user's account page
@app.route('/account', methods=["GET", "POST"])
@login_required
def account():

    form = UpdateAccountInfo()
    # Logic for updating user account info
    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated successfully", 'success')

        return redirect(url_for('account'))

    # Populate form fields w/ users's current info
    elif request.method == "GET":

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.profile_image_file_name)

    return render_template('account.html', title="Account", image_file=image_file, form=form)