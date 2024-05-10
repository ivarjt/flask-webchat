from app import admin, User, db, Friendship, Room, Message
from flask_admin.contrib.sqla import ModelView
from app import app
from flask_login import current_user
from flask import request, abort, redirect

def is_superuser():
    """
    Checks if the current user is a superuser.

    Returns:
        bool: True if the current user is a superuser or if the superuser status of a user is updated successfully, False otherwise.
    """
    if not current_user.is_superuser:
        return False

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)

        if user:
            user.is_superuser = True if request.form.get('is_superuser') == 'on' else False
            db.session.commit()

    return True

class CustomModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_superuser:
            return True
        else:
            abort(403)

admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Friendship, db.session))
admin.add_view(CustomModelView(Room, db.session))
admin.add_view(CustomModelView(Message, db.session))


@app.route("/admin/redirect", methods=['GET', 'POST'])
def admin_redirect():
    return redirect("/admin/")
