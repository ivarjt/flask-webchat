from app import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from ..forms import FriendRequestForm
from ..models import Friendship, User
from flask_login import current_user
from wtforms.validators import ValidationError

@app.route("/send_friend_request", methods=["GET", "POST"])
def send_friend_request(): #TODO: This could possibly be cleaned up by returning from models.py
    form = FriendRequestForm()

    if form.validate_on_submit():
        #TODO: REMOVE DEBUG PRINTS
        receiver_id = Friendship.convert_username_to_user_id(form.username.data)
        print(f"Receiver ID: {receiver_id}")
        receiver = User.query.get(receiver_id)
        print(f"Receiver Object: {receiver}")

        if receiver is not None:  # Ensure the receiver exists
            if current_user.id == receiver_id:
                flash("You cannot send a friend request to yourself.", "error")
            elif Friendship.query.filter(
                (Friendship.sender_id == current_user.id) &
                (Friendship.receiver_id == receiver_id) &
                (Friendship.status == 'pending')
            ).first():
                flash("You have already sent a friend request to this person.", "error")
            elif Friendship.query.filter(
                ((Friendship.sender_id == receiver_id) & (Friendship.receiver_id == current_user.id)) |
                ((Friendship.sender_id == current_user.id) & (Friendship.receiver_id == receiver_id))
            ).filter(Friendship.status == 'accepted').first():
                flash("You are already friends with this person.", "error")
            else:
                friendship_instance = Friendship()
                friendship_instance.send_friend_request(sender_id=current_user.id, receiver=receiver)
                flash("Friend request sent.", "success")
                return redirect(url_for("success"))
        else:
            flash("This username does not exist. Please try again.", "error")

    return render_template("friends/send_friend_request.html", form=form)


@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
def accept_friend_request(request_id):
    # Call the accept_friend_request function
    result = Friendship.accept_friend_request(request_id)

    # Flash a message to indicate the result
    if result == "Friend request accepted.":
        flash("Friend request accepted.", "success")
    else:
        flash("Friend request not found.", "error")

    # Redirect the user to the appropriate page
    return redirect(url_for('home'))


@app.route('/reject_friend_request/<int:request_id>', methods=['POST'])
def reject_friend_request(request_id):
    # Call the reject_friend_request function
    result = Friendship.reject_friend_request(request_id)

    # Flash a message to indicate the result
    if result == "Friend request rejected.":
        flash("Friend request rejected.", "success")
    else:
        flash("Friend request not found.", "error")

    # Redirects the user
    return redirect(url_for('home'))


@app.route("/handle_friend_request")
def handle_friend_request():
    incoming_requests = current_user.get_incoming_friend_requests()
    return render_template("friends/handle_friend_request.html", incoming_requests=incoming_requests)


@app.route("/success")  # FIXME: temporary
def success():
    return render_template("friends/success.html")


@app.route("/list_friends")
def list_friends():
    friends = Friendship.get_friends(current_user.id)

    # Render the template with the list of friends
    return render_template("friends/remove_friend.html", friends=friends)


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

    return redirect(url_for('success'))
