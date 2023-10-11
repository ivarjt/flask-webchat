from app import app, socketio
from flask import render_template, redirect, url_for, request


@app.route("/login", methods=["POST", "GET"])
def login():
    
    return render_template("login.html")
    
    # if the method is POST and Username is admin then 
    # it will redirects to success url. 
    #if request.method == "POST" and request.form["username"] == "admin": 
     #   return redirect(url_for("success")) 
  
    # if the method is GET or username is not admin, 
    # then it redirects to index method. 
    #return redirect(url_for('login')) 
  

@app.route("/login/check", methods=["POST"])
def login_check():
    return "<h1>TESTING<\h1>"