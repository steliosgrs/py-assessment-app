"""
Authentication utilities for the application.
"""

import secrets
from typing import Optional, Dict, Any, Tuple

from shared.models import User
from shared.db import get_db_session


def create_user(
    username: str, email: str, password: str
) -> Tuple[bool, str, Optional[User]]:
    """
    Create a new user in the database.

    Args:
        username (str): Username for the new user
        email (str): Email for the new user
        password (str): Password for the new user

    Returns:
        Tuple[bool, str, Optional[User]]:
            - Success status (bool)
            - Message (str)
            - User object if created successfully, None otherwise
    """
    db = get_db_session()

    # Check if username or email already exists
    existing_user = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )

    if existing_user:
        return False, "Username or email already exists", None

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True, "User created successfully", new_user
    except Exception as e:
        db.rollback()
        return False, f"Error creating user: {str(e)}", None


def authenticate_user(
    username_or_email: str, password: str
) -> Tuple[bool, str, Optional[User]]:
    """
    Authenticate a user with username/email and password.

    Args:
        username_or_email (str): Username or email of the user
        password (str): Password to check

    Returns:
        Tuple[bool, str, Optional[User]]:
            - Success status (bool)
            - Message (str)
            - User object if authenticated successfully, None otherwise
    """
    db = get_db_session()

    # Find user by username or email
    user = (
        db.query(User)
        .filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        )
        .first()
    )

    if not user:
        return False, "Invalid username or email", None

    if not user.check_password(password):
        return False, "Invalid password", None

    if not user.is_active:
        return False, "Account is inactive", None

    return True, "Authentication successful", user


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Get a user by ID.

    Args:
        user_id (int): User ID to look up

    Returns:
        Optional[User]: User object if found, None otherwise
    """
    db = get_db_session()
    return db.query(User).filter(User.id == user_id).first()


def generate_session_token() -> str:
    """
    Generate a secure session token.

    Returns:
        str: Secure random token
    """
    return secrets.token_hex(32)
