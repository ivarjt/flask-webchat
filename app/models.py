from app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    participant = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date_created = db.Column(db.Date, default=datetime.utcnow)
    
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
    
    #FIXME: Innan man skapar ett rum kontrolelra om det finns
    def create_room(room_creator, participant):
        new_room = Room(room_creator=room_creator, participant=participant)
        db.session.add(new_room)
        db.session.commit()
        
    def check_if_room_exists(room_creator, participant):
        room = Room.query.filter_by(room_creator=room_creator, participant=participant).first()
        room_reversed = Room.query.filter_by(room_creator=participant, participant=room_creator).first()
        
        if room is None and room_reversed is None:
            return True
        else:
            return False

        
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    is_superuser = db.Column(db.Boolean, default=False)
    image_link = db.Column(db.String(255), nullable=False)

    # Constructor method to initialize User objects
    def __init__(self, username, email, password, is_superuser, image_link):
        self.username = username
        self.password = password
        self.email = email
        self.is_superuser = is_superuser
        self.image_link = image_link
    
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
    status = db.Column(db.String(20), nullable=False, default="pending")  # 'pending', 'accepted', 'rejected'

    # Define relationships between sender and receiver and User model
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    def send_friend_request(self, sender_id, receiver): #FIXME: Check the weird empty returns
        """
        Send a friend request from the sender to the receiver.

        Args:
            sender_id (int): The user ID sending the friend request.
            receiver (User): The user receiving the friend request.
        """
        if sender_id == receiver.id:
            print("Cannot send friend request to oneself.")
            return

        existing_receiver = User.query.get(receiver.id)
        #TODO: REMOVE DEBUG PRINTS
        print("-"*50)
        print(existing_receiver)
        print("-"*50)
        if not existing_receiver:
            print("Receiver does not exist.")
            return "Receiver does not exist."
        
        existing_request = Friendship.query.filter_by(sender_id=sender_id, receiver_id=receiver.id).first()
        existing_request_reversed = Friendship.query.filter_by(sender_id=receiver.id, receiver_id=sender_id).first()


        if existing_request:
            if existing_request.status == "rejected":
                existing_request.status = "pending"
                db.session.commit()
                print("Friend request sent again.")
            else:
                print("Friend request already sent.")
            return
        
        #TODO: This wont return anything to the user on the screen
        if existing_request_reversed:
            if existing_request_reversed.status == "rejected":
                existing_request_reversed.status = "pending"
                db.session.commit()
                print("Friend request sent again.")
            else:
                print("Friend request already sent.")
            return

        user = User.query.get(receiver.id)
        if not user:
            print("User doesn't exist.")
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
        friend_request = Friendship.query.filter(
            (Friendship.sender_id == current_user) & (Friendship.receiver_id == friend) |
            (Friendship.sender_id == friend) & (Friendship.receiver_id == current_user),
            Friendship.status == "accepted"
        ).first()

        if friend_request:
            # Delete the friendship record from the database
            db.session.delete(friend_request)
            db.session.commit()

            return "Friend removed."
        else:
            return "Friend not found."