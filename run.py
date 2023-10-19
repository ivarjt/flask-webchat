import os
from app import app, socketio, db

if __name__ == "__main__":
    database_file = os.path.join(app.instance_path, "db.sqlite3")

    if not os.path.exists(database_file):
        print("Database file does not exist. Creating a new one...")
        with app.app_context():
            db.create_all()
            
    socketio.run(app, debug=True, host="0.0.0.0")
