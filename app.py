from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from os import getenv
from dotenv import load_dotenv
from blog.forms import RegistrationForm, LoginForm
from datetime import datetime
from blog.models import Post, User
from blog import ENV, app



if __name__ == '__main__':

    if ENV == 'dev':
        app.run(debug=True)
    else:
        pass