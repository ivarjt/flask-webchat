from functools import wraps
from flask import abort, current_app
from flask_login import current_user

def is_superuser_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()

        if current_user.is_superuser != 1:
            abort(403)

        return view_function(*args, **kwargs)

    return decorated_function
