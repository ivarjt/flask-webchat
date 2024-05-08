from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User
from .utils.helpers import validate_password

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=100), validate_password], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    # Validate if the username is already taken
    # If a user with the same username exists, raise a validation error
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is already taken. Please choose a different one.")

    # Validate if the email is already registered
    # If an account with the same email exists, raise a validation error
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("An account with this email already exists. Please use a different email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=100)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[InputRequired(), Length(min=8, max=100)], render_kw={"placeholder": "Old Password"})
    new_password = PasswordField("New Password", validators=[InputRequired(), Length(min=8, max=100), validate_password], render_kw={"placeholder": "New Password"})
    submit = SubmitField("Change Password")

class FriendRequestForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Enter Username"})
    submit = SubmitField("Send Friend Request")


    # Validate if the username is already taken
    # If a user with the same username exists, raise a validation error
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("This username does not exist. Please try again.")
    