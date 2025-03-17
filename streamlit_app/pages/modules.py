"""
Modules page for Streamlit application - displays Python modules & lessons.
"""

import streamlit as st
import sys
import os
import markdown
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.firebase import get_all_modules, get_module_by_id, mark_module_completed

# Initialize the session state if not already done
if "user_id" not in st.session_state:
    st.session_state.user_id = None


def render_markdown(md_content):
    """Render markdown content in Streamlit"""
    html = markdown.markdown(
        md_content, extensions=["fenced_code", "codehilite", "tables"]
    )
    st.markdown(html, unsafe_allow_html=True)


def load_module_content(module_id):
    """Load module content from Firestore"""
    module = get_module_by_id(module_id)

    if not module:
        st.error("Module not found!")
        return

    st.session_state.current_module = module

    # Display module content
    st.title(module.get("title", "Module"))

    # Display the module content as markdown
    render_markdown(module.get("content", "No content available"))

    # Mark as completed button
    if st.button("Mark as Completed"):
        success = mark_module_completed(st.session_state.user_id, module_id)
        if success:
            st.success("Module marked as completed!")
            # Refresh user state if needed
            st.experimental_rerun()
        else:
            st.error("Failed to mark module as completed!")

    # Link to exercises
    st.write("Ready to practice?")
    if st.button("Go to Exercises"):
        st.switch_page("pages/exercises.py")


def display_module_list():
    """Display list of all modules"""
    st.title("Python Learning Modules")

    modules = get_all_modules()

    if not modules:
        st.info("No modules available yet!")
        return

    # Get user data to check completed modules
    user_completed_modules = []
    if "user" in st.session_state and st.session_state.user:
        user_completed_modules = st.session_state.user.get("completedModules", [])

    # Display module cards
    for module in modules:
        col1, col2 = st.columns([4, 1])

        with col1:
            title = module.get("title", "Untitled Module")
            description = module.get("description", "No description")

            # Check if completed
            module_id = module.get("id")
            is_completed = module_id in user_completed_modules

            # Display completion status
            if is_completed:
                st.markdown(f"### ✅ {title}")
            else:
                st.markdown(f"### {title}")

            st.write(description)

        with col2:
            if st.button("Open", key=f"open_{module.get('id')}"):
                st.session_state.selected_module = module.get("id")
                st.experimental_rerun()


def main():
    """Main function for the modules page."""
    # Check if logged in
    if st.session_state.user_id is None:
        st.warning("Please log in to access the modules.")
        if st.button("Go to Login"):
            st.switch_page("pages/login.py")
        return

    # Initialize module state if needed
    if "selected_module" not in st.session_state:
        st.session_state.selected_module = None

    # Display navigation in sidebar
    with st.sidebar:
        st.title("Navigation")
        if st.button("Back to Home"):
            st.switch_page("app.py")
        if st.button("Exercises"):
            st.switch_page("pages/exercises.py")

        # Show "All Modules" button if a specific module is selected
        if st.session_state.selected_module:
            if st.button("All Modules"):
                st.session_state.selected_module = None
                st.experimental_rerun()

    # Display modules list or specific module
    if st.session_state.selected_module:
        load_module_content(st.session_state.selected_module)
    else:
        display_module_list()


if __name__ == "__main__":
    main()
