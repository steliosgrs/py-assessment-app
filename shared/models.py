"""
SQLAlchemy models for the application.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from shared.db import Base


class User(Base):
    """
    User model for authentication.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def set_password(self, password):
        """
        Set the password hash from a plaintext password.

        Args:
            password (str): Plaintext password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check a plaintext password against the stored hash.

        Args:
            password (str): Plaintext password to check

        Returns:
            bool: True if the password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Convert user model to dictionary representation.

        Returns:
            dict: User data dictionary
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"<User {self.username}>"
