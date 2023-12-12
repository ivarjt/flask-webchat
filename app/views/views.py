from app import app, db
from flask import render_template, request, url_for, redirect
from flask_login import current_user

@app.route("/")
@app.route("/home")
def home():
    """
    TODO: This is the debugging homepage and will later be replaced with the actual homepage
    if the user is logged in, it will render the homepage and say that the user is logged in and display their username
    if the user is not logged in, it will render the homepage and say that the user is not logged in
    """
    if current_user.is_authenticated:
        return render_template("home.html", user=current_user)
    return render_template("home.html", user=None)

@app.route("/update_image_link", methods=['POST'])
def update_image_link():
    if current_user.is_authenticated:
        image_link = request.form.get('image_link')

        # You may want to add validation logic here to ensure the link is valid

        # Update the user's image_link in the database
        current_user.image_link = image_link
        db.session.commit()

    return redirect(url_for('home'))


@app.route("/new_home")
def new_home():
    return render_template("new_home.html")

#For debbuging purposes
@app.route("/layout")
def layout():
    return render_template("chat/layout.html")