from app import app, socketio, db
from flask import render_template, redirect, url_for, request
from flask_socketio import rooms, emit, join_room, leave_room
from flask_login import current_user
from ..models import Room, Friendship, Message

@app.route("/chat/<int:room_id>")
def chat(room_id):  
    return render_template("chat/chat.html", username=current_user.username, room_id=room_id)

@app.route("/create_room/<string:user2_name>", methods=["POST"])
def create_room(user2_name):
    user1_id = current_user.id
    user2_id = Friendship.convert_username_to_user_id(user2_name)
    
    existing_room = Room.room_exists(user1_id, user2_id)
    if existing_room:
        # Room already exists
            return redirect(url_for('chat', room_id=existing_room.id))
    
    room = Room(user1_id=user1_id, user2_id=user2_id)
    db.session.add(room)
    db.session.commit()
    
    return redirect(url_for("chat", room_id=room.id))


@socketio.on('connect')
def on_connect(auth):
    if auth.get("token" ) != "123":
        raise ConnectionRefusedError("Unauthorized")

@socketio.on('message')
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    room = data.get('room')

    # Save the message to the database
    if room in rooms():
        new_message = Message(
            user_id=current_user.id,
            room_id=room,
            message=message
        )
        db.session.add(new_message)
        db.session.commit()

    # Broadcast the message to all participants in the room
    emit("message", {"username": username, "message": message}, to=room)
        
@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    
    # Join the room
    join_room(room)
    
    # Load messages for the room from the database
    messages = Message.query.filter_by(room_id=room).all()
    
    # Emit each message to the user who joined the room
    for message in messages:
        emit("message", {"username": message.user.username, "message": message.message}, to=request.sid)

@socketio.on('leave')
def on_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit("leave", {"username": username}, to=room)
