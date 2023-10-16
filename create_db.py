from app import app, db, User
from datetime import datetime

app.app_context().push()

db.create_all()


