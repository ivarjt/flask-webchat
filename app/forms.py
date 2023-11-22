from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User
import re

def validate_password(Form, field):
    password = field.data

    password_requirements = """Password must contain at least one lowercase character.<br>
                                Password must contain at least one uppercase character.<br>
                                Password must contain at least one digit.<br>
                                Password must contain at least one special character."""



    # Check if the password contains at least one lowercase character
    if not re.search(r'[a-z]', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one uppercase character
    if not re.search(r'[A-Z]', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one digit (integer)
    if not re.search(r'\d', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one special character (you can customize the special characters)
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\\-]', password):
        raise ValidationError(password_requirements)


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=100), validate_password], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("This username is already taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("An account with this email already exists. Please use a different email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=100)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class FriendRequestForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    submit = SubmitField("Send Friend Request")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("This username does not exist. Please try again.")
    