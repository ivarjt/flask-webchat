from app import admin, User, db
from flask_admin.contrib.sqla import ModelView
from app import app
from flask_login import current_user
from flask import request, abort

def is_superuser():
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

@app.route("/admin/test", methods=['GET', 'POST'])
def admin_test():
    return "hello"
