from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # Filter by "username"
        if user is not None:
            raise ValidationError("This username is already taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("An account with this email already exists. Please use a different email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Length(max=100)], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
