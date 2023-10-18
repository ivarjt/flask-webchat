from app import app, socketio, db, login_manager
from flask import render_template, redirect, url_for
from flask_socketio import SocketIO, send
from flask_login import login_user, login_required, current_user
from .models import User
        
# Chat room
@app.route("/")
def index():
    return render_template("index.html", username=current_user.username)

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    send({'sender': sender, 'message': message}, broadcast=True)