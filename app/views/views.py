from app import app
from flask import render_template
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

@app.route("/new_home")
def new_home():
    return render_template("new_home.html")

#For debbuging purposes
@app.route("/layout")
def layout():
    return render_template("chat/layout.html")