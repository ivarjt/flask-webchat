import os
from app import app, socketio, db, RUN_IN_DEBUG_MODE, HOST
from colorama import Fore, Style

# Check if the script is being run directly
if __name__ == "__main__":
    # Define path to database file
    database_file = os.path.join(app.instance_path, "db.sqlite3")

    # Check if database file already exists
    if not os.path.exists(database_file):
        # Alerts the user that the database file does not exist and is being created
        print(f"{Fore.RED}Database file does not exist. Creating a new one...{Style.RESET_ALL}")
        
        # Create the database file
        with app.app_context():
            db.create_all()
            
    # Run the Flask application with SocketIO
    socketio.run(app, debug=RUN_IN_DEBUG_MODE, host=HOST)
