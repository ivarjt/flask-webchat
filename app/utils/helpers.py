import random 
from wtforms.validators import ValidationError
import re

def get_profile_picture():
    """
    Returns a random profile picture URL from a list of profile pictures.

    Returns:
        str: The URL of a randomly selected profile picture.
    """
    pfp_list = ["https://raw.githubusercontent.com/ivarjt/flask-webchat-media/main/default-pfp/moose_profile_blue.png",
                "https://raw.githubusercontent.com/ivarjt/flask-webchat-media/main/default-pfp/moose_profile_green.png",
                "https://raw.githubusercontent.com/ivarjt/flask-webchat-media/main/default-pfp/moose_profile_red.png",
                "https://raw.githubusercontent.com/ivarjt/flask-webchat-media/main/default-pfp/moose_profile_yellow.png"]
    return random.choice(pfp_list)


def validate_password(Form, field):
    """
    Validates the password based on the following requirements:
    - Password must contain at least one lowercase character.
    - Password must contain at least one uppercase character.
    - Password must contain at least one digit.
    - Password must contain at least one special character.

    Args:
        Form (class): The form class.
        field (object): The password field object.

    Raises:
        ValidationError: If the password does not meet the requirements.

    Returns:
        None
    """
    password = field.data

    password_requirements = """Password must contain at least one lowercase character.<br>
                                Password must contain at least one uppercase character.<br>
                                Password must contain at least one digit.<br>
                                Password must contain at least one special character."""

    # Check if the password contains at least one lowercase character
    if not re.search(r'[a-z]', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one uppercase character
    if not re.search(r'[A-Z]', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one digit (integer)
    if not re.search(r'\d', password):
        raise ValidationError(password_requirements)

    # Check if the password contains at least one special character (you can customize the special characters)
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\\-]', password):
        raise ValidationError(password_requirements)
    