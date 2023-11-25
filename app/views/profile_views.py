from app import app
from flask import render_template
from ..models import User
    
#TODO: FIX A GOOD PROFILE PAGE
@app.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile/profile_page.html', user=user)
