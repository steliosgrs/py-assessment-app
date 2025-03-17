"""
Main Streamlit application entry point with Firebase integration.
"""

import streamlit as st
import sys
import os
import dotenv

dotenv.load_dotenv()
DEBUG = os.environ.get("DEBUG")
print(f"Mode Debug: {DEBUG}")
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.firebase import initialize_firebase, get_user_by_id, get_all_modules

# Initialize the session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Initialize Firebase
if not DEBUG:
    firebase_initialized = initialize_firebase()
    if not firebase_initialized:
        st.error("Firebase initialization failed. Please check your credentials.")


def is_authenticated():
    if DEBUG:
        return True
    """Check if the user is authenticated."""
    return st.session_state.user_id is not None


def get_current_user():
    if DEBUG:
        return {
            "uid": "4350934509344u503",
            "email": "stelios@uniwa.gr",
            "displayName": "Stelios Georgaras",
        }
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
    if "selected_exercise" in st.session_state:
        st.session_state.selected_exercise = None
    if "selected_exercise_data" in st.session_state:
        st.session_state.selected_exercise_data = None

    # TODO: Do not rerun just clear the login user
    # st.experimental_rerun()


def main():
    """Main application entry point."""
    # Sidebar with login/logout and navigation
    with st.sidebar:
        st.title("Navigation")

        # Display user info or login/register options
        if is_authenticated():
            user = get_current_user()
            if user:
                st.success(
                    f"Logged in as: {user.get('displayName', user.get('email', 'User'))}"
                )
                st.button("Logout", on_click=logout)

                # Navigation links
                st.write("## Menu")
                st.page_link("app.py", label="Home")
                st.page_link("pages/modules.py", label="Learning Modules")
                st.page_link("pages/exercises.py", label="Exercises")
                # Add more navigation links as needed
            else:
                st.error("User data not found. Please log in again.")
                st.session_state.user_id = None
                # st.experimental_rerun()
        else:
            st.info("Please log in to access the application")
            st.page_link("pages/login.py", label="Login")
            st.page_link("pages/register.py", label="Register")

    # Main content
    if is_authenticated():
        # Display protected content
        user = get_current_user()
        if user:
            st.title(f"Welcome to Python Learning, {user.get('displayName', 'User')}!")
            st.write(
                "This platform will help you learn Python programming through interactive modules and exercises."
            )

            # Progress information
            st.subheader("Your Progress")

            # Get modules and exercises data
            # modules = get_all_modules()
            # total_modules = len(modules)
            modules = []
            total_modules = 1

            # Calculate completion
            completed_modules = user.get("completedModules", [])
            completed_exercises = user.get("completedExercises", [])

            # Progress bars
            st.write("Module completion:")
            module_progress = len(completed_modules) / max(total_modules, 1) * 100
            st.progress(module_progress / 100)
            st.write(
                f"{len(completed_modules)} of {total_modules} modules completed ({int(module_progress)}%)"
            )

            # Quick navigation
            st.subheader("Quick Navigation")
            col1, col2 = st.columns(2)

            with col1:
                st.write("Continue learning")
                if st.button("Go to Modules"):
                    st.switch_page("pages/modules.py")

            with col2:
                st.write("Practice your skills")
                if st.button("Go to Exercises"):
                    st.switch_page("pages/exercises.py")

            # Recently completed
            if completed_modules or completed_exercises:
                st.subheader("Recent Activity")

                # Show last completed module if any
                if completed_modules:
                    st.write("Last completed module:")
                    last_module_id = completed_modules[-1]
                    for module in modules:
                        if module.get("id") == last_module_id:
                            st.write(f"• {module.get('title')}")
                            break

            # Feature explanation
            st.subheader("Features")
            st.markdown(
                """
            - **Learning Modules**: Interactive Python lessons with code examples
            - **Exercises**: Practice problems with automated testing
            - **Progress Tracking**: Keep track of your completed modules and exercises
            """
            )
    else:
        # Display public content
        st.title("Welcome to the Python Learning Platform")
        st.write(
            "Please log in or register to access the interactive learning modules and exercises."
        )

        # Benefits of the platform
        st.subheader("Why Use Our Platform?")
        st.markdown(
            """
        - Learn Python at your own pace
        - Interactive coding exercises with instant feedback
        - Track your progress as you learn
        - Practice with real-world examples
        """
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                st.switch_page("pages/login.py")
        with col2:
            if st.button("Register"):
                st.switch_page("pages/register.py")


if __name__ == "__main__":
    main()
