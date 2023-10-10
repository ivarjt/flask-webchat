from app import app, socketio
from flask import render_template
from flask_socketio import SocketIO, send

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    send({'sender': sender, 'message': message}, broadcast=True)