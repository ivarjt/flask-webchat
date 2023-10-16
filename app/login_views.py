from app import app, socketio
from flask import render_template, redirect, url_for, request


@app.route("/login")
def login():
    return render_template("authentication/login.html")

@app.route("/register")
def register():
    return render_template("authentication/register.html")