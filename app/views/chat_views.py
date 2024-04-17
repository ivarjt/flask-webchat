from app import app, socketio
from flask import render_template, redirect, url_for
from flask_socketio import rooms, emit, join_room, leave_room
from flask_login import current_user
from ..models import Room
        
# Chat room
"""
@app.route("/chat")
def chat():
    if current_user.is_authenticated:
        return render_template("chat/index.html", username=current_user.username)
    return redirect(url_for("login"))

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    send({'sender': sender, 'message': message}, broadcast=True) """

@app.route("/chat1")
def chat1():  
    return render_template("chat/chat1.html", username=current_user.username)
#TODO: Make so only correct user can go on chat1 and chat2
@app.route("/chat2")
def chat2():  
    return render_template("chat/chat2.html", username=current_user.username)

@socketio.on('connect')
def on_connect(auth):
    if auth.get("token" ) != "123":
        raise ConnectionRefusedError("Unauthorized")

@socketio.on('message')
def handle_message(data):
    username= data.get('username')
    message = data.get('message')
    room = data.get('room')
    if room in rooms():
        emit("message", {"username": username, "message": message}, to=room)
        
@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    emit("join", {"username": username}, to=room)
    
@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit("leave", {"username": username}, to=room)
    
    
@app.route("/create_room/<string:participant>", methods=["POST"])
def create_room(participant):
    # Convert the username to a user ID
    room_creator_id = current_user.id
    participant_id = Room.convert_username_to_user_id(participant)
    print("BDHFSDKNFSD: "+str(participant_id))

    
    room_doesnt_exist = Room.check_if_room_exists(room_creator_id, participant_id)
    
    if room_doesnt_exist:
        Room.create_room(room_creator_id, participant_id)
    
    return redirect(url_for("chat1"))


"""
@app.route("/remove_friend/<string:friend>", methods=["POST"])
def remove_friend(friend):
    # Convert the username to a user ID
    friend = Friendship.convert_username_to_user_id(friend)

    # Call the remove_friend function
    result = Friendship.remove_friend(current_user.id, friend)

    # Flash a message to indicate the result
    if result == "Friend removed.":
        flash("Friend removed.", "success")
    else:
        flash("Friend not found.", "error")

    return redirect(url_for('success'))"""