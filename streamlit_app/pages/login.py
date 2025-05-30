"""
Login page for Streamlit application with Firebase authentication.
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.firebase import authenticate_user

# Initialize the session state if not already done
if "user_id" not in st.session_state:
    st.session_state.user_id = None


def login_user(email, password):
    """
    Attempt to log in a user with Firebase.

    Args:
        email (str): Email
        password (str): Password
    """
    success, message, user = authenticate_user(email, password)

    if success and user:
        st.session_state.user_id = user.get("uid")
        st.success(message)
        # Redirect to the main page
        st.switch_page("app.py")
    else:
        st.error(message)


def main():
    st.title("Login")

    # Check if already logged in
    if st.session_state.user_id is not None:
        st.success("You are already logged in.")
        st.button("Go to Home", on_click=lambda: st.switch_page("app.py"))
        return

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email")

        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                login_user(email, password)

    # Link to registration
    st.write("Don't have an account?")
    if st.button("Register"):
        st.switch_page("pages/register.py")

    # Back to home
    if st.button("Back to Home"):
        st.switch_page("app.py")


main()
