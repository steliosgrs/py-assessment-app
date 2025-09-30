"""
Database layer initialization and repository factory.
Automatically provides correct repository implementations based on environment.
"""

import os
from typing import Literal

# Import repository interfaces
from shared.database.repositories.user_repository import IUserRepository

# from shared.database.repositories.module_repository import IModuleRepository
# from shared.database.repositories.exercise_repository import IExerciseRepository


class RepositoryFactory:
    """
    Factory for creating repository instances based on environment.
    Implements strategy pattern for database selection.
    """

    # Cache instances to ensure singletons
    _user_repo_instance = None
    # _module_repo_instance = None
    # _exercise_repo_instance = None

    @staticmethod
    def get_database_type() -> Literal["mongodb", "firestore"]:
        """
        Determine which database to use from environment variable.

        Returns:
            "mongodb" or "firestore"

        Environment Variables:
            DATABASE: "mongodb" or "firestore" (default: "firestore")
            DEV: "true" to force MongoDB (legacy support)
        """
        # Check DATABASE env variable first
        db_type = os.environ.get("DATABASE", "").lower()

        # Legacy support: DEV=true means MongoDB
        if os.environ.get("DEV", "").lower() in ("true", "1", "yes"):
            db_type = "mongodb"

        # Default to firestore for production
        if db_type not in ("mongodb", "firestore"):
            db_type = "firestore"

        return db_type

    @classmethod
    def create_user_repository(cls) -> IUserRepository:
        """
        Create and return appropriate user repository implementation.
        Returns cached instance (singleton pattern).

        Returns:
            IUserRepository: Either MongoUserStore or FirestoreUserStore
        """
        if cls._user_repo_instance is not None:
            return cls._user_repo_instance

        db_type = cls.get_database_type()

        if db_type == "mongodb":
            print("🔧 Using MongoDB for user repository")
            from shared.database.mongodb.user_store import MongoUserStore

            cls._user_repo_instance = MongoUserStore()
        else:
            print("🔥 Using Firestore for user repository")
            from shared.database.firestore.user_store import FirestoreUserStore

            cls._user_repo_instance = FirestoreUserStore()

        return cls._user_repo_instance

    # @classmethod
    # def create_module_repository(cls) -> IModuleRepository:
    #     """
    #     Create and return appropriate module repository implementation.
    #     Returns cached instance (singleton pattern).

    #     Returns:
    #         IModuleRepository: Either MongoModuleStore or FirestoreModuleStore
    #     """
    #     if cls._module_repo_instance is not None:
    #         return cls._module_repo_instance

    #     db_type = cls.get_database_type()

    #     if db_type == "mongodb":
    #         print("🔧 Using MongoDB for module repository")
    #         from shared.database.mongodb.module_store import MongoModuleStore

    #         cls._module_repo_instance = MongoModuleStore()
    #     else:
    #         print("🔥 Using Firestore for module repository")
    #         from shared.database.firestore.module_store import FirestoreModuleStore

    #         cls._module_repo_instance = FirestoreModuleStore()

    #     return cls._module_repo_instance

    # @classmethod
    # def create_exercise_repository(cls) -> IExerciseRepository:
    #     """
    #     Create and return appropriate exercise repository implementation.
    #     Returns cached instance (singleton pattern).

    #     Returns:
    #         IExerciseRepository: Either MongoExerciseStore or FirestoreExerciseStore
    #     """
    #     if cls._exercise_repo_instance is not None:
    #         return cls._exercise_repo_instance

    #     db_type = cls.get_database_type()

    #     if db_type == "mongodb":
    #         print("🔧 Using MongoDB for exercise repository")
    #         from shared.database.mongodb.exercise_store import MongoExerciseStore

    #         cls._exercise_repo_instance = MongoExerciseStore()
    #     else:
    #         print("🔥 Using Firestore for exercise repository")
    #         from shared.database.firestore.exercise_store import FirestoreExerciseStore

    #         cls._exercise_repo_instance = FirestoreExerciseStore()

    #     return cls._exercise_repo_instance

    @classmethod
    def reset_instances(cls):
        """
        Reset cached instances (useful for testing).
        Forces new instances to be created on next call.
        """
        cls._user_repo_instance = None
        # cls._module_repo_instance = None
        # cls._exercise_repo_instance = None


# Create singleton instances on module import
# These will be used throughout the application
user_repo = RepositoryFactory.create_user_repository()
# module_repo = RepositoryFactory.create_module_repository()
# exercise_repo = RepositoryFactory.create_exercise_repository()


# Utility function to get current database info
def get_database_info() -> dict:
    """
    Get information about current database configuration.

    Returns:
        dict: Database type and connection info
    """
    db_type = RepositoryFactory.get_database_type()

    info = {
        "type": db_type,
        "user_repo": user_repo.__class__.__name__,
        # "module_repo": module_repo.__class__.__name__,
        # "exercise_repo": exercise_repo.__class__.__name__,
    }

    if db_type == "mongodb":
        info["connection"] = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        info["database"] = os.environ.get("MONGODB_NAME", "python_learning_dev")
    else:
        info["credentials"] = os.environ.get(
            "FIREBASE_CREDENTIALS", "firebase-credentials.json"
        )

    return info


def print_database_info():
    """Print current database configuration to console."""
    info = get_database_info()
    print("\n" + "=" * 60)
    print(f"DATABASE CONFIGURATION")
    print("=" * 60)
    print(f"Type: {info['type'].upper()}")
    print(f"User Repository: {info['user_repo']}")
    print(f"Module Repository: {info['module_repo']}")
    print(f"Exercise Repository: {info['exercise_repo']}")

    if info["type"] == "mongodb":
        print(f"Connection: {info['connection']}")
        print(f"Database: {info['database']}")
    else:
        print(f"Credentials: {info['credentials']}")

    print("=" * 60 + "\n")


# Export public API
__all__ = [
    # Repository instances (main exports)
    "user_repo",
    "module_repo",
    "exercise_repo",
    # Factory class (for advanced usage)
    "RepositoryFactory",
    # Utility functions
    "get_database_info",
    "print_database_info",
    # Interfaces (for type hints)
    "IUserRepository",
    "IModuleRepository",
    "IExerciseRepository",
]
