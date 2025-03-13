"""
Registration page for Streamlit application.
"""

import streamlit as st
import sys
import os
import re

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.auth import create_user


def is_valid_email(email):
    """
    Validate email format.

    Args:
        email (str): Email to validate

    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_username(username):
    """
    Validate username format.

    Args:
        username (str): Username to validate

    Returns:
        bool: True if valid, False otherwise
    """
    # Only allow alphanumeric characters and underscores
    pattern = r"^[a-zA-Z0-9_]{3,20}$"
    return re.match(pattern, username) is not None


def register_user(username, email, password, confirm_password):
    """
    Register a new user.

    Args:
        username (str): Username
        email (str): Email
        password (str): Password
        confirm_password (str): Password confirmation
    """
    # Validate input
    if not username or not email or not password or not confirm_password:
        st.error("Please fill in all fields.")
        return

    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    if not is_valid_email(email):
        st.error("Please enter a valid email address.")
        return

    if not is_valid_username(username):
        st.error(
            "Username must be 3-20 characters and can only contain letters, numbers, and underscores."
        )
        return

    if len(password) < 8:
        st.error("Password must be at least 8 characters long.")
        return

    # Create user
    success, message, user = create_user(username, email, password)

    if success:
        st.success(message)
        # Redirect to login page after successful registration
        st.button("Go to Login", on_click=lambda: st.switch_page("pages/login.py"))
    else:
        st.error(message)


def main():
    """Main function for the registration page."""
    st.title("Register")

    # Check if already logged in
    if "user_id" in st.session_state and st.session_state.user_id is not None:
        st.success("You are already logged in.")
        st.button("Go to Home", on_click=lambda: st.switch_page("app.py"))
        return

    # Registration form
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit_button = st.form_submit_button("Register")

        if submit_button:
            register_user(username, email, password, confirm_password)

    # Link to login
    st.write("Already have an account?")
    if st.button("Login"):
        st.switch_page("pages/login.py")

    # Back to home
    if st.button("Back to Home"):
        st.switch_page("app.py")


if __name__ == "__main__":
    main()
