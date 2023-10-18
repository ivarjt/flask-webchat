from app import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    is_superuser = db.Column(db.Boolean, default=False)

    # Constructor method to initialize User objects
    def __init__(self, username, email, password, is_superuser):
        self.username = username
        self.password = password
        self.email = email
        self.is_superuser = is_superuser
    
    # Dunder method that returns a string representation of all users
    def __repr__(self):
        return f"<User: id={self.id}, name={self.username}, email={self.email}, date_joined={self.date_joined}>, is_superuser={self.is_superuser}\n"