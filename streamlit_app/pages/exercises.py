"""
Exercises page for Streamlit application - loads exercises from local files.
"""

import streamlit as st
import sys
import os
import markdown
from pathlib import Path
import io

# Add the project root to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import from local file system instead of Firebase
from utils.course_loader import (
    get_all_modules,
    get_module_by_id,
    get_exercises_by_module,
    get_exercise_by_id,
    get_test_file_for_exercise,
    mark_exercise_completed,
)
from utils.exercise_runner import test_exercise
from utils.firebase import get_user_by_id  # Still need this for user data

# Initialize the session state if not already done
if "user_id" not in st.session_state:
    st.session_state.user_id = None


def render_markdown(md_content):
    """Render markdown content in Streamlit"""
    html = markdown.markdown(
        md_content, extensions=["fenced_code", "codehilite", "tables"]
    )
    st.markdown(html, unsafe_allow_html=True)


def display_exercise(exercise_id):
    """Display a specific exercise"""
    # Get full exercise data
    exercise_data = get_exercise_by_id(exercise_id)

    if not exercise_data:
        st.error("Exercise not found!")
        return

    st.title(exercise_data.get("title", "Exercise"))

    # Display the description as markdown
    st.subheader("Instructions")
    render_markdown(exercise_data.get("description", "No description available"))

    # Code template or starter code if provided
    starter_code = exercise_data.get("starterCode", "# Your code here")

    # Allow code submission
    st.subheader("Your Solution")

    # Initialize session state for code editor if not already done
    if "code_solution" not in st.session_state:
        st.session_state.code_solution = starter_code

    # Code editor
    user_code = st.text_area(
        "Edit your code below:", value=st.session_state.code_solution, height=300
    )

    # Update session state with current code
    st.session_state.code_solution = user_code

    # File uploader as an alternative
    st.write("Or upload your solution file:")
    uploaded_file = st.file_uploader("Choose a Python file", type=["py"])

    # Submit button
    submit_button = st.button("Submit & Test")

    if submit_button:
        # Determine which code to test
        if uploaded_file is not None:
            # Use uploaded file content
            exercise_content = uploaded_file.getvalue()
        else:
            # Use code from text editor
            exercise_content = user_code.encode("utf-8")

        # Get test file for this exercise
        test_success, test_message, test_content = get_test_file_for_exercise(
            exercise_id
        )

        if not test_success:
            st.error(f"Failed to get test file: {test_message}")
            return

        # Run tests
        success, messages = test_exercise(exercise_content, test_content)

        # Display results
        if success:
            st.success("✅ All tests passed! Great job!")

            # Mark exercise as completed
            mark_success = mark_exercise_completed(
                st.session_state.user_id, exercise_id
            )
            if mark_success:
                st.success("Exercise marked as completed in your profile!")

            # Show detailed test results
            # with st.expander("View detailed test results"):
            #     for message in messages:
            #         st.write(message)
        else:
            st.error("❌ Some tests failed. Check the details and try again.")

            # Show detailed test results
            # st.subheader("Test Results")
            # for message in messages:
            #     st.text(message)


def display_exercise_list(module_id):
    """Display list of exercises for a specific module"""
    # Get module info
    module = get_module_by_id(module_id)
    if not module:
        st.error("Module not found!")
        return

    st.title(f"Exercises: {module.get('title', 'Module')}")

    # Get exercises for this module
    print(f"MODULE_ID {module_id}")
    exercises = get_exercises_by_module(module_id)

    if not exercises:
        st.info("No exercises available for this module yet!")
        return

    # Get user data to check completed exercises
    user_completed_exercises = []
    if "user" in st.session_state and st.session_state.user:
        user_completed_exercises = st.session_state.user.get("completedExercises", [])

    # Display exercise cards
    for exercise in exercises:
        col1, col2 = st.columns([4, 1])

        with col1:
            title = exercise.get("title", "Untitled Exercise")
            difficulty = exercise.get("difficulty", "Medium")

            # Check if completed
            exercise_id = exercise.get("id")
            is_completed = exercise_id in user_completed_exercises

            # Display completion status
            if is_completed:
                st.markdown(f"### ✅ {title}")
            else:
                st.markdown(f"### {title}")

            st.write(f"Difficulty: {difficulty}")

        with col2:
            if st.button("Start", key=f"start_{exercise.get('id')}"):
                st.session_state.selected_exercise = exercise.get("id")
                # st.experimental_rerun()


def run():

    # Check if logged in
    if st.session_state.user_id is None:
        st.warning("Please log in to access the exercises.")
        if st.button("Go to Login"):
            st.switch_page("pages/login.py")
        return

    # Initialize exercise state if needed
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = None

    if "selected_exercise" not in st.session_state:
        st.session_state.selected_exercise = None

    # Display navigation in sidebar
    with st.sidebar:
        st.title("Navigation")
        if st.button("Back to Home"):
            st.switch_page("app.py")
        if st.button("Modules"):
            st.switch_page("pages/modules.py")

        # Module selection
        st.subheader("Select Module")
        modules = get_all_modules()
        module_titles = {module.get("id"): module.get("title") for module in modules}

        for module_id, title in module_titles.items():
            if st.button(title, key=f"nav_{module_id}"):
                st.session_state.selected_module = module_id
                st.session_state.selected_exercise = None
                # st.experimental_rerun()

        # Back to exercise list if an exercise is selected
        if st.session_state.selected_exercise:
            if st.button("Back to Exercise List"):
                st.session_state.selected_exercise = None
                # st.experimental_rerun()

    # Display content based on state
    if st.session_state.selected_exercise:
        # Display specific exercise
        display_exercise(st.session_state.selected_exercise)
    elif st.session_state.selected_module:
        # Display exercises for selected module
        display_exercise_list(st.session_state.selected_module)
    else:
        # No module selected, show module selection
        st.title("Python Exercises")
        st.write("Select a module from the sidebar to view its exercises.")

        # Display all modules as cards
        modules = get_all_modules()

        for module in modules:
            col1, col2 = st.columns([4, 1])

            with col1:
                title = module.get("title", "Untitled Module")
                description = module.get("description", "No description")

                st.markdown(f"### {title}")
                st.write(description)

            with col2:
                if st.button("View Exercises", key=f"view_{module.get('id')}"):
                    st.session_state.selected_module = module.get("id")
                    # st.experimental_rerun()
