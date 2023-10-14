from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    
    # Constructor method to initialize User objects
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    # Dunder method that returns a string representation of all users
    def __repr__(self):
        return f"<User: id={self.id}, name={self.name}, email={self.email}, date_joined={self.date_joined}>\n"
