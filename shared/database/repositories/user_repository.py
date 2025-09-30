"""
User repository interface - defines contract for user operations
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple, List


class IUserRepository(ABC):
    """
    Abstract interface for user data operations.
    All user storage implementations must implement this interface.
    """

    @abstractmethod
    def create_user(
        self, email: str, password: str, display_name: str
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Create a new user account"""
        pass

    @abstractmethod
    def authenticate_user(
        self, email: str, password: str
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Authenticate user with email and password"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by their unique ID"""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by their email"""
        pass

    @abstractmethod
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user fields"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Delete a user account"""
        pass
