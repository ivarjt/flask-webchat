# Non Local Imports 
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

# Flask app config
app = Flask(__name__)

# SocketIO
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # To reduse some terminal spam, could be turned to True if needed for debugging
db = SQLAlchemy(app)

# Admin
admin = Admin() 
admin.init_app(app)

#---------------------
# Local Imports Below
#---------------------

# Models
from .models import User

# Views
from app import views, admin_views, login_views

"""
    
    from app import app, db, User

app_ctx = app.app_context()
app_ctx.push()

db.create_all()

app_ctx.pop()

User.query.all()

"""