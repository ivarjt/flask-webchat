from app import app
from flask import render_template

@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(403)
def error_handler(error):
    error_code = getattr(error, 'code', 500)  # Default to 500 if no code is provided
    return render_template('error_pages/error.html', error_code=error_code), error_code