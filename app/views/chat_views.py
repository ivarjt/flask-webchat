from app import app, socketio
from flask import render_template, redirect, url_for
from flask_socketio import send
from flask_login import current_user
        
# Chat room
@app.route("/chat")
def chat():
    if current_user.is_authenticated:
        return render_template("chat/index.html", username=current_user.username)
    return redirect(url_for("login"))

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    send({'sender': sender, 'message': message}, broadcast=True)