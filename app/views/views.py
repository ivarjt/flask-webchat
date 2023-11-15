from app import app
from flask import render_template

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#For debbuging purposes
@app.route("/layout")
def layout():
    return render_template("chat/layout.html")

