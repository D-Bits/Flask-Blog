from flask import render_template, redirect, url_for, flash
from blog.forms import RegistrationForm, LoginForm
from blog import app


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
