import streamlit as st

# Hide default Streamlit navigation

from utils.manage_account import register_user
from utils.firebase import (
    authenticate_user,
    create_user,
    initialize_firebase,
    get_user_by_id,
)

# # Initialize the session state
# if "user_id" not in st.session_state:
#     st.session_state.user_id = None

# Initialize Firebase
firebase_initialized = initialize_firebase()
if not firebase_initialized:
    st.error("Firebase initialization failed. Please check your credentials.")


# Function to log in a user
def login_user(email, password):
    """
    Attempt to log in a user with Firebase.
    """
    success, message, user = authenticate_user(email, password)

    if success and user:
        st.session_state.user_id = user.get("uid")
        st.success(message)
        # Refresh the page to show the logged-in state
        st.rerun()
    else:
        st.error(message)


def is_authenticated():
    """Check if the user is authenticated."""
    return st.session_state.user_id is not None


def get_current_user():
    """Get the current authenticated user."""
    if is_authenticated():
        user_data = get_user_by_id(st.session_state.user_id)
        # Store in session state for easy access across pages
        st.session_state.user = user_data
        return user_data
    return None


def logout():
    """Log out the current user."""
    st.session_state.user_id = None
    st.session_state.user = None
    # Clear any module or exercise selections
    if "selected_module" in st.session_state:
        st.session_state.selected_module = None


# Display user profile when logged in
def display_user_profile():
    """Display user profile information when logged in."""
    user = get_user_by_id(st.session_state.user_id)

    if not user:
        st.error("Error loading user profile. Please log out and log in again.")
        return

    st.title("Your Account")

    # Display basic user info
    st.header("Profile Information")
    st.write(f"**Name:** {user.get('displayName', 'Not set')}")
    st.write(f"**Email:** {user.get('email', 'Not available')}")

    # Progress section
    st.header("Your Progress")

    # Completed modules
    completed_modules = user.get("completedModules", [])
    st.subheader("Completed Modules")
    if completed_modules:
        for module_id in completed_modules:
            st.write(f"- Module ID: {module_id}")
    else:
        st.write("You haven't completed any modules yet.")

    # Completed exercises
    completed_exercises = user.get("completedExercises", [])
    st.subheader("Completed Exercises")
    if completed_exercises:
        for exercise_id in completed_exercises:
            st.write(f"- Exercise ID: {exercise_id}")
    else:
        st.write("You haven't completed any exercises yet.")

    # Account actions
    st.header("Account Actions")
    if st.button("Logout"):
        logout()


# Display login form
def display_login_form():
    """Display the login form for unauthenticated users."""
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                login_user(email, password)

    # Option to switch to registration view
    st.write("Don't have an account?")
    if st.button("Register Instead"):
        st.session_state.account_view = "register"
        st.rerun()


# Display registration form
def display_registration_form():
    """Display the registration form for new users."""
    st.title("Create Account")

    with st.form("register_form"):
        display_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit_button = st.form_submit_button("Register")

        if submit_button:
            register_user(display_name, email, password, confirm_password)

    # Option to switch to login view
    st.write("Already have an account?")
    if st.button("Login Instead"):
        st.session_state.account_view = "login"
        # st.rerun()


def run():
    # Initialize account view state if not present
    if "account_view" not in st.session_state:
        st.session_state.account_view = "login"

    # Check if user is logged in
    if st.session_state.user_id is not None:
        # User is logged in, display profile
        display_user_profile()
    else:
        # User is not logged in, show login or registration based on state
        if st.session_state.account_view == "login":
            display_login_form()
        else:
            display_registration_form()
