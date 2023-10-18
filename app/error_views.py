from app import app
from flask import render_template

@app.errorhandler(404) 
def error_404(e):
    return render_template("error_pages/error_404.html"), 404

@app.errorhandler(403) 
def error_403(e):
    return render_template("error_pages/error_403.html"), 403