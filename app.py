from flask import Flask, render_template, flash, redirect, url_for
from os import getenv
from dotenv import load_dotenv
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
# Set secret key
app.config['SECRET_KEY'] = getenv("SECRET_KEY")

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

    form = RegistrationForm()

    return render_template('login.html', form=form, title="Login")


if __name__ == '__main__':

    if ENV == 'dev':
        app.run(debug=True)
    else:
        pass