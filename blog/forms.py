from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User


# For registering new users
class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Make sure username is unique
    def validate_username(self, username):

        user = User.query.filter_by(username.data).first()

        if user:

            raise ValidationError('That username is already taken. Please choose a different one.')

    # Make sure email is unique
    def validate_email(self, email):

        email = User.query.filter_by(email.data).first()

        if email:

            raise ValidationError('That email is already taken. Please choose a different one.')


# For logging in existing users
class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')