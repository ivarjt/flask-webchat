from app import admin, User, db
from flask_admin.contrib.sqla import ModelView

# Adds the admin page to edit users
admin.add_view(ModelView(User, db.session))