from app import app
from flask import render_template
from flask_login import current_user

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#For debbuging purposes
@app.route("/layout")
def layout():
    return render_template("chat/layout.html")

@app.route('/status')
def status():
    if current_user.is_authenticated:
        message = 'You are logged in'
    else:
        message = 'You are not logged in'
    return message