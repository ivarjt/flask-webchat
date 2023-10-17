from app import admin, User, db
from flask_admin.contrib.sqla import ModelView
from .decorators import is_superuser_required
from flask import render_template


# Adds the admin page to edit users
admin.add_view(ModelView(User, db.session))