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
    
    def get_incoming_friend_requests(self):
        return Friendship.query.filter_by(receiver_id=self.id, status='pending').all()
    
    
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # 'pending', 'accepted', 'rejected'

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
        friend_request = Friendship.query.get(request_id)
        
        if friend_request:
            friend_request.status = "accepted"
            db.session.commit()
            
            return "Friend request accepted."
        else:
            return "Friend request not found."

    
    def reject_friend_request():
        pass
    
    def get_friends(user_id):
        friends = Friendship.query.filter(
                    (Friendship.sender_id == user_id) | (Friendship.receiver_id == user_id),
                    Friendship.status == "accepted"
                ).all()
        

        # Extract the usernames of the friends
        friend_usernames = [friend.sender.username if friend.receiver_id == user_id else friend.receiver.username for friend in friends]

        return friend_usernames
    
    @staticmethod
    def convert_username_to_user_id(username):
        user = User.query.filter_by(username=username).first()
        return user.id