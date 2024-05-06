from app import app
from flask import render_template, request, redirect, url_for, flash
from ..models import db, Friendship, User
from flask_login import current_user
from ..utils.helpers import get_profile_picture
from ..forms import FriendRequestForm

@app.route("/settings")
@app.route("/settings/account")
def account_settings():
    return render_template('settings/account_settings.html', user=current_user)

@app.route("/settings/friends", methods=["GET", "POST"])
def friends_settings():
    friends = Friendship.get_friends(current_user.id)
    sent_requests = Friendship.sent_friend_request(current_user.id)
    incoming_requests = current_user.get_incoming_friend_requests()
    friend_data = Friendship.get_friends_with_image(current_user.id)

    form = FriendRequestForm()
    if form.validate_on_submit():
        receiver_id = Friendship.convert_username_to_user_id(form.username.data)
        receiver = User.query.get(receiver_id)
        if receiver is not None:
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
                return redirect(url_for("friends_settings"))

        else:
            flash("This username does not exist. Please try again.", "error")

    return render_template('settings/friend_settings.html', friends=friends, sent_requests=sent_requests, incoming_requests=incoming_requests, form=form, friend_data=friend_data)



@app.route("/update_image_link", methods=['POST'])
def update_image_link():
    if current_user.is_authenticated:
        image_link = request.form.get('image_link')
        
        if image_link == "":
            image_link = get_profile_picture() 

        # You may want to add validation logic here to ensure the link is valid

        # Update the user's image_link in the database
        current_user.image_link = image_link
        db.session.commit()

    return redirect(url_for('account_settings'))