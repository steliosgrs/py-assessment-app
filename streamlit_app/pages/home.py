import streamlit as st

# from pages.account import is_authenticated, get_current_user, logout
# from utils.course_loader import (
#     get_all_modules,
#     get_module_by_id,
#     mark_module_completed,
# )

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.database import get_database_info

into = get_database_info()  # For logging purposes

print(f"🌐 Database Info: {into}")


def run():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    # Main content
    # if is_authenticated():
    #     # Display protected content
    #     user = get_current_user()
    #     if user:
    #         st.title(f"Welcome to PyCamp 🐍, {user.get('displayName', 'User')}!")
    #         st.write(
    #             "This platform will help you learn Python programming through interactive modules and exercises."
    #         )

    #         # Progress information
    #         st.subheader("Your Progress")

    #         # Get modules data
    #         modules = get_all_modules()
    #         total_modules = len(modules)

    #         # Calculate completion
    #         completed_modules = user.get("completedModules", [])
    #         completed_exercises = user.get("completedExercises", [])

    #         # Progress bars
    #         st.write("Module completion:")
    #         module_progress = len(completed_modules) / max(total_modules, 1) * 100
    #         st.progress(module_progress / 100)
    #         st.write(
    #             f"{len(completed_modules)} of {total_modules} modules completed ({int(module_progress)}%)"
    #         )

    #         # Quick navigation
    #         st.subheader("Quick Navigation")
    #         col1, col2 = st.columns(2)

    #         with col1:
    #             st.write("Continue learning")
    #             if st.button("Go to Modules"):
    #                 st.switch_page("pages/modules.py")

    #         with col2:
    #             st.write("Practice your skills")
    #             if st.button("Go to Exercises"):
    #                 st.switch_page("pages/1_exercises.py")

    #         # Recently completed
    #         if completed_modules or completed_exercises:
    #             st.subheader("Recent Activity")

    #             # Show last completed module if any
    #             if completed_modules:
    #                 st.write("Last completed module:")
    #                 last_module_id = completed_modules[-1]
    #                 for module in modules:
    #                     if module.get("id") == last_module_id:
    #                         st.write(f"• {module.get('title')}")
    #                         break

    #         # Feature explanation
    #         st.subheader("Features")
    #         st.markdown(
    #             """
    #         - **Learning Modules**: Interactive Python lessons with code examples
    #         - **Exercises**: Practice problems with automated testing
    #         - **Progress Tracking**: Keep track of your completed modules and exercises
    #         """
    #         )
    # else:
    # Display public content
    st.title("Welcome to the PyCamp Platform")
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
