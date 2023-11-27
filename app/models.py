from app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    is_superuser = db.Column(db.Boolean, default=False)

    # Constructor method to initialize User objects
    def __init__(self, username, email, password, is_superuser):
        self.username = username
        self.password = password
        self.email = email
        self.is_superuser = is_superuser
    
    # Dunder method that returns a string representation of all users
    def __repr__(self):
        return f"<User: id={self.id}, name={self.username}, email={self.email}, date_joined={self.date_joined}>, is_superuser={self.is_superuser}\n"
    
    # Function to get incoming friend requests for a user
    def get_incoming_friend_requests(self):
        return Friendship.query.filter_by(receiver_id=self.id, status='pending').all()
    
    
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # 'pending', 'accepted', 'rejected', 'removed'

    # Define relationships between sender and receiver and User model
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    def send_friend_request(self, sender_id, receiver):
        """
        Send a friend request from the sender to the receiver.

        Args:
            sender_id (int): The user ID sending the friend request.
            receiver (User): The user receiving the friend request.
        """
        existing_request = Friendship.query.filter_by(sender_id=sender_id, receiver_id=receiver.id).first()

        if existing_request:
            print("Friend request already sent.")
            return

        new_request = Friendship(sender_id=sender_id, receiver_id=receiver.id, status="pending")
        db.session.add(new_request)
        db.session.commit()        

    
    def accept_friend_request(request_id):
        """
        Accept a friend request.

        Args:
            request_id (int): The ID of the friend request.

        Returns:
            str: A message indicating whether the friend request was accepted or not.
        """
        friend_request = Friendship.query.get(request_id)
        
        if friend_request:
            friend_request.status = "accepted"
            db.session.commit()
            
            return "Friend request accepted."
        else:
            return "Friend request not found."
    
    def get_friends(user_id):
        """
        Get the usernames of the friends of a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of usernames of the user's friends.
        """
        friends = Friendship.query.filter(
                    (Friendship.sender_id == user_id) | (Friendship.receiver_id == user_id),
                    Friendship.status == "accepted"
                ).all()
        

        # Extract the usernames of the friends
        friend_usernames = [friend.sender.username if friend.receiver_id == user_id else friend.receiver.username for friend in friends]

        return friend_usernames
    
    @staticmethod
    def convert_username_to_user_id(username):
        """
            Convert a username to a user ID.

            Args:
                username (str): The username to convert.

            Returns:
                int: The user ID corresponding to the username.
            """
        user = User.query.filter_by(username=username).first()
        return user.id
    
    def reject_friend_request(request_id):
        """
        Reject a friend request.

        Args:
            request_id (int): The ID of the friend request to reject.

        Returns:
            str: A message indicating the result of the rejection.
        """

        friend_request = Friendship.query.get(request_id)
        
        if friend_request:
            friend_request.status = "rejected"
            db.session.commit()
            
            return "Friend request rejected."
        else:
            return "Friend request not found."
    
    def remove_friend(current_user, friend):
        """
        Remove a friend from the current user's friend list.

        Args:
            current_user (int): The ID of the current user.
            friend (int): The ID of the friend to be removed.

        Returns:
            str: A message indicating that the friend has been removed.
        """

        # Find the friendship record using current_user and friend ID's
        friend_request = Friendship.query.filter_by(sender_id=current_user, receiver_id=friend, status="accepted").first()

        # Update the status to "removed" and commit the changes
        friend_request.status = "removed"
        db.session.commit()
        
        return "Friend removed."
        
        