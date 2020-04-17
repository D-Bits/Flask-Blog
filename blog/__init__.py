from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from os import getenv
from dotenv import load_dotenv


# Load env vars from .env file
load_dotenv()

app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = getenv("SECRET_KEY")
# Set SQL Alchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# Initialize Bcrypt for user auth
bcrypt = Bcrypt(app)
# Initialize login manager
login_manager = LoginManager(app)
# Set a login route
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Load environment type from environment var
ENV = getenv("ENV")


from blog import routes