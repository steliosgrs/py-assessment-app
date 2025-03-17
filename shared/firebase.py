"""
Firebase utilities for authentication and user progress tracking only.
Module and exercise content is stored locally to reduce database operations.
"""

import os
import json
import requests
from typing import Optional, Dict, Any, Tuple
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Firebase authentication endpoint
FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

# Global variable to store firebase admin app


def initialize_firebase():
    firebase_admin_app = None
    """
    Initialize Firebase Admin SDK using credentials from environment variable or file.
    """
    # global firebase_admin_app
    cred_path = os.environ.get("FIREBASE_CREDENTIALS", "firebase-credentials.json")

    # Check if Firebase Admin is already initialized
    if not firebase_admin._apps:
        # If credentials are provided as a file
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            try:
                firebase_admin_app = firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Error initializing Firebase Admin from file: {e}")
                return False
        else:
            print(f"Firebase credentials not found at {cred_path}")
            return False

    return True


def _get_api_key():
    """Get Firebase Web API Key from environment variable"""
    api_key = os.environ.get("FIREBASE_API_KEY")
    if not api_key:
        print("FIREBASE_API_KEY environment variable not set")
        return None
    return api_key


# Authentication functions
def create_user(
    email: str, password: str, display_name: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Create a new user in Firebase Authentication.

    Args:
        email (str): User email
        password (str): User password
        display_name (str): User display name

    Returns:
        Tuple[bool, str, Optional[Dict]]:
            - Success status (bool)
            - Message (str)
            - User data if created successfully, None otherwise
    """
    if not initialize_firebase():
        return False, "Firebase initialization failed", None

    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            email_verified=False,
        )

        # Create user document in Firestore
        db = firestore.client()
        user_ref = db.collection("users").document(user.uid)
        user_ref.set(
            {
                "email": email,
                "displayName": display_name,
                "createdAt": firestore.SERVER_TIMESTAMP,
                "completedModules": [],
                "completedExercises": [],
            }
        )

        user_data = {
            "uid": user.uid,
            "email": user.email,
            "displayName": user.display_name,
        }

        return True, "User created successfully", user_data
    except auth.EmailAlreadyExistsError:
        return False, "Email already exists", None
    except Exception as e:
        return False, f"Error creating user: {str(e)}", None


def authenticate_user(
    email: str, password: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticate a user using Firebase Auth REST API.

    Args:
        email (str): User email
        password (str): User password

    Returns:
        Tuple[bool, str, Optional[Dict]]:
            - Success status (bool)
            - Message (str)
            - User data if authenticated successfully, None otherwise
    """
    # Initialize Firebase Admin SDK
    if not initialize_firebase():
        return False, "Firebase initialization failed", None

    # Get API key
    api_key = _get_api_key()
    if not api_key:
        return False, "Firebase API key not configured", None

    try:
        # Use the REST API to sign in with email/password
        signin_url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={api_key}"
        signin_payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }

        response = requests.post(signin_url, json=signin_payload)
        data = response.json()

        if "error" in data:
            error_message = data["error"].get("message", "Authentication failed")
            if error_message == "EMAIL_NOT_FOUND":
                return False, "Email not found", None
            elif error_message == "INVALID_PASSWORD":
                return False, "Invalid password", None
            else:
                return False, f"Authentication error: {error_message}", None

        # Get the user ID from the response
        user_id = data.get("localId")
        id_token = data.get("idToken")

        if not user_id:
            return False, "Failed to get user ID from authentication response", None

        # Get user details from Firebase Admin SDK
        user_record = auth.get_user(user_id)

        # Get additional user data from Firestore
        db = firestore.client()
        user_doc = db.collection("users").document(user_id).get()

        user_data = {
            "uid": user_id,
            "email": user_record.email,
            "displayName": user_record.display_name or email.split("@")[0],
            "token": id_token,
        }

        # Add Firestore data if it exists
        if user_doc.exists:
            firestore_data = user_doc.to_dict()
            # Don't override existing fields
            for key, value in firestore_data.items():
                if key not in user_data:
                    user_data[key] = value

        return True, "Authentication successful", user_data

    except requests.exceptions.RequestException as e:
        return False, f"Network error during authentication: {str(e)}", None
    except Exception as e:
        return False, f"Authentication error: {str(e)}", None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by ID from Firebase.

    Args:
        user_id (str): Firebase user ID

    Returns:
        Optional[Dict]: User data if found, None otherwise
    """
    if not initialize_firebase():
        return None

    try:
        user = auth.get_user(user_id)

        # Get additional user data from Firestore
        db = firestore.client()
        user_doc = db.collection("users").document(user_id).get()

        user_data = {
            "uid": user.uid,
            "email": user.email,
            "displayName": user.display_name,
        }

        if user_doc.exists:
            firestore_data = user_doc.to_dict()
            user_data.update(firestore_data)

        return user_data
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting user: {str(e)}")
        return None


# User progress tracking
def mark_module_completed(user_id: str, module_id: str) -> bool:
    """
    Mark a module as completed for a user.

    Args:
        user_id (str): User ID
        module_id (str): Module ID

    Returns:
        bool: Success status
    """
    if not initialize_firebase():
        return False

    try:
        db = firestore.client()
        user_ref = db.collection("users").document(user_id)

        # Get current user data
        user_doc = user_ref.get()
        if not user_doc.exists:
            return False

        user_data = user_doc.to_dict()
        completed_modules = user_data.get("completedModules", [])

        # Add module to completed list if not already there
        if module_id not in completed_modules:
            completed_modules.append(module_id)
            user_ref.update({"completedModules": completed_modules})

        return True
    except Exception as e:
        print(f"Error marking module as completed: {str(e)}")
        return False


def mark_exercise_completed(user_id: str, exercise_id: str) -> bool:
    """
    Mark an exercise as completed for a user.

    Args:
        user_id (str): User ID
        exercise_id (str): Exercise ID

    Returns:
        bool: Success status
    """
    if not initialize_firebase():
        return False

    try:
        db = firestore.client()
        user_ref = db.collection("users").document(user_id)

        # Get current user data
        user_doc = user_ref.get()
        if not user_doc.exists:
            return False

        user_data = user_doc.to_dict()
        completed_exercises = user_data.get("completedExercises", [])

        # Add exercise to completed list if not already there
        if exercise_id not in completed_exercises:
            completed_exercises.append(exercise_id)
            user_ref.update({"completedExercises": completed_exercises})

        return True
    except Exception as e:
        print(f"Error marking exercise as completed: {str(e)}")
        return False
