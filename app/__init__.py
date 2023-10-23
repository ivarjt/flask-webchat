# Non Local Imports 
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

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

# Bcrypt
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#---------------------
# Local Imports Below
#---------------------

# Models
from .models import User

# Views
from .views import chat_views, admin_views, login_views, profile_views, error_views, views