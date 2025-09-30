"""
Registration page for Streamlit application with Firebase authentication.
"""

import streamlit as st
from pydantic import ValidationError

# Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utils.manage_account import register_user


def main():
    st.title("Register")
    st.markdown("**Only academic emails addresses are accepted!**")
    st.markdown("Please use your **@ieee.org** email")
    success = None
    message = "User not created successfully."
    # Check if already logged in
    if "user_id" in st.session_state and st.session_state.user_id is not None:
        st.success("You are already logged in.")
        st.button("Go to Home", on_click=lambda: st.switch_page("app.py"))
        return

    # Registration form
    with st.form("register_form"):
        st.subheader("Create Your Account")

        display_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            help="This will be displayed in the application",
        )
        email = st.text_input(
            "University Email",
            placeholder="your_email@ieee.org",
            help="Only @ieee.org email addresses are accepted",
        )
        col1, col2 = st.columns(2)
        password = col1.text_input(
            "Password", type="password", help="Must be at least 6 characters long"
        )
        confirm_password = col2.text_input(
            "Confirm Password", type="password", help="Re-enter your password"
        )
        submit_button = st.form_submit_button("Register", type="primary")

        if submit_button:
            # Basic client-side validation
            if not all([display_name, email, password, confirm_password]):
                st.error("Please fill in all fields.")
            else:

                success, message, user = register_user(
                    display_name, email, password, confirm_password
                )
        else:
            message = ""

    if success:
        st.success(message)
        # TODO: Email Verification
        st.info("Please check your email to verify your account.")
        # Show login button after successful registration
        # Redirect to login page after successful registration
        # TODO: Fix the bug that the login page doesn't show up according to:
        # https://discuss.streamlit.io/t/st-switch-page-wont-work-if-it-is-nested-in-another-if-statement/69385/3
        if st.button("Go to Login"):
            st.switch_page("pages/login.py")

    else:
        if message:
            st.error(message)

    # Navigation
    st.divider()
    have_account, back_home = st.columns(2)

    # Link to login
    with have_account:
        st.write("Already have an account?")
        if st.button("Login"):
            st.switch_page("pages/login.py")

    # Back to home
    with back_home:
        st.write("Want to go back?")
        if st.button("Back to Home"):
            st.switch_page("app.py")


main()
