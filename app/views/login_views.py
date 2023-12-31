from app import app, bcrypt, db
from flask import render_template, redirect, url_for
from ..forms import LoginForm, RegisterForm
from ..models import User
from flask_login import login_user, logout_user, login_required
from ..utils.helpers import get_profile_picture

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
    
    return render_template("authentication/login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data) # Hash the password
        new_user = User(username=form.username.data,
                        password=hashed_password,
                        email=form.email.data,
                        is_superuser=0,
                        image_link=get_profile_picture())
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("login"))
        
    return render_template("authentication/register.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
