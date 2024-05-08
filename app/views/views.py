from app import app, db
from flask import render_template, redirect, url_for
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
        return redirect(url_for("friends_settings"))
    return render_template("new_home.html", user=None)


@app.route("/new_home")
def new_home():
    return redirect(url_for("home"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/safety")
def safety():
    return render_template("safety.html")

