from app import app, bcrypt, db
from flask import render_template, request, redirect, url_for, flash
from ..models import db, Friendship, User
from flask_login import current_user
from ..utils.helpers import get_profile_picture
from ..forms import FriendRequestForm, ChangePasswordForm

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

@app.route("/settings/change_password", methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        #FIXME: KOLLA SÅ GAMMLA LÖSENORDET STÄMMER MED DET I DATABASEN
        old_password_db_enc = user.password
        old_password_form = form.old_password.data
        new_password = form.new_password.data
        
        if bcrypt.check_password_hash(old_password_db_enc, form.old_password.data):
            # Update the user's password in the database
            user.password = bcrypt.generate_password_hash(form.new_password.data)
            db.session.commit()
            flash("Password updated successfully!", "success")
        else:
            flash("The password you entered is incorrect. Please try again.", "error")
        
        print_sexy(old_password_form, old_password_db_enc, new_password) #FIXME: REMOVE THIS LATER, DEBUG FUNCTION
        

    return render_template('settings/change_password_settings.html', form=form)

#FIXME: REMOVE THIS LATER, DEBUG FUNCTION
def print_sexy(old_pass, old_pass_enc, new_pass):
    print("-"*50)
    print(f"Your old password is [TYPED]: {old_pass}") # The one you typed in the form
    print(f"Your old password is [ENC]: {old_pass_enc}") # The one stored in the database (Encrypted)
    print(f"Your new password is: {new_pass}") # The new password you typed in the form
    print("-"*50)


@app.route("/password_updated", methods=['GET', 'POST'])
def password_updated():
    return "<h1>Password updated successfully!</h1>" #FIXME: to proper route or remove

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