from app import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from ..forms import FriendRequestForm
from ..models import Friendship, User
from flask_login import current_user
from wtforms.validators import ValidationError


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
    return redirect(url_for('friends_settings'))


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
    return redirect(url_for('friends_settings'))


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
    return render_template("friends/remove_friend.html", friends=friends) #FIXME: This should be list_friends.html


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

    return redirect(url_for('friends_settings'))

@app.route("/cancel_friend_request/<string:request_id>", methods=["POST"])
def cancel_friend_request(request_id):
    
    request_name = Friendship.convert_username_to_user_id(request_id)
    
    result = Friendship.cancel_friend_request(current_user.id, request_name)

    if result == "Friend request cancelled.":
        print("Friend request cancelled.", "success")
    else:
        print("Friend request not found.", "error")

    return redirect(url_for('friends_settings'))