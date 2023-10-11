from flask import Flask, g
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from app import views, admin_views, login_views
