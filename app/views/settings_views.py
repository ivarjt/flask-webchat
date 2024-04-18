from app import app
from flask import render_template, request, redirect, url_for
from ..models import db
from flask_login import current_user


#TODO:REMOVE THIS
@app.route("/settings")
@app.route("/settings/account")
def account_settings():
    return render_template('settings/account_settings.html', user=current_user)

@app.route("/update_image_link", methods=['POST'])
def update_image_link():
    if current_user.is_authenticated:
        image_link = request.form.get('image_link')

        # You may want to add validation logic here to ensure the link is valid

        # Update the user's image_link in the database
        current_user.image_link = image_link
        db.session.commit()

    return redirect(url_for('account_settings'))