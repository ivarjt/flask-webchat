from app import app
from flask import render_template, redirect, url_for, flash
from ..forms import FriendRequestForm
from ..models import Friendship, User
from flask_login import current_user

@app.route("/send_friend_request", methods=["GET", "POST"])
def send_friend_request():
    form = FriendRequestForm()
    
    if form.validate_on_submit():
        friendship_instance = Friendship()
        receiver_id = Friendship.convert_username_to_user_id(form.username.data)
        friendship_instance.send_friend_request(sender_id=current_user.id, receiver=User.query.get(receiver_id))
        return redirect(url_for("success"))

    return render_template("friends/send_friend_request.html", form=form)

@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
def accept_friend_request(request_id):
    # Call the accept_friend_request function
    result = Friendship.accept_friend_request(request_id)

    # Flash a message to indicate the result (you can customize this part)
    if result == "Friend request accepted.":
        flash("Friend request accepted.", "success")
    else:
        flash("Friend request not found.", "error")

    # Redirect the user to the appropriate page
    return redirect(url_for('home'))

@app.route("/list_friends")
def list_friends():
    friends = Friendship.get_friends(current_user.id)

    # Render the template with the list of friends
    return render_template("friends/list_friends.html", friends=friends)

@app.route("/handle_friend_request")
def handle_friend_request():
    incoming_requests = current_user.get_incoming_friend_requests()
    return render_template("friends/handle_friend_request.html", incoming_requests=incoming_requests)

@app.route("/success") #temporary
def success():
    return render_template("friends/success.html")