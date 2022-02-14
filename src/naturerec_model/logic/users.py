"""
User business logic
"""

import hashlib
import os
import base64
import sqlalchemy as db
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..model import Session, User

def _check_for_existing_records(session, username):
    """
    Return the IDs for existing records with the specified name

    :param session: SQLAlchemy session on which to perform the query
    :param username: Username to match
    :returns: A collection of user IDs for the matching records
    """
    users = session.query(User).filter(User.username == username).all()
    return [user.id for user in users]


def create_user(username, password):
    """
    Create a new user

    :param username: Username
    :param password: Password
    :returns: An instance of the User class for the created record
    :raises ValueError: If the specified name is None, an empty string or consists solely of whitespace
    :raises ValueError: If the specified password is None, an empty string or consists solely of whitespace
    :raises ValueError: If the username is a duplicate
    """
    cleaned_password = password.strip() if password else None
    if not cleaned_password:
        raise ValueError("Invalid password")

    try:
        with Session.begin() as session:
            # There is a check constraint to prevent duplicates in the Python model but the pre-existing database
            # does not have that constraint so explicitly check for duplicates before adding a new record
            tidied = "".join(username.split()).casefold() if username else None
            if len(_check_for_existing_records(session, tidied)):
                raise ValueError("Duplicate username found")

            # Hash the password with a random salt
            salt = os.urandom(32)
            hashed_password = hashlib.pbkdf2_hmac("sha256", cleaned_password.encode("utf-8"), salt, 100000)

            # Convert to Base-64 for storage
            b64salt = base64.b64encode(salt).decode("utf-8")
            b64password = base64.b64encode(hashed_password).decode("utf-8")

            # Create the user
            user = User(username=tidied, salt=b64salt, password=b64password)
            session.add(user)
    except IntegrityError as e:
        raise ValueError("Invalid or duplicate user") from e

    return user


def authenticate(username, password):
    try:
        # Retrieve the named user
        with Session.begin() as session:
            user = session.query(User).filter(User.username == username).one()
    except NoResultFound:
        raise ValueError("Authentication error")

    # Hash the supplied password and check for a match
    salt = base64.b64decode(user.salt.encode("utf-8"))
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    b64password = base64.b64encode(hashed_password).decode("utf-8")

    if b64password != user.password:
        raise ValueError("Authentication error")
