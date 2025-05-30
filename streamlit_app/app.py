import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

load_dotenv()
from pages import home, account, modules, exercises, about


def main():
    # TEST
    with st.sidebar:
        app = "Home"
        app = option_menu(
            menu_title="PyCamp",
            options=[
                "Home",
                "Account",
                "Modules",
                "Exercises",
                "About us",
            ],
            icons=[
                "house-fill",
                "person-circle",
                "book-fill",
                "file-earmark-code-fill",
                "info-circle-fill",
            ],
            menu_icon="braces",
            default_index=0,
            # styles={
            #     "container": {"padding": "5!important", "background-color": "orange"},
            #     "icon": {"color": "white", "font-size": "23px"},
            #     "nav-link": {
            #         "color": "white",
            #         "font-size": "20px",
            #         "text-align": "left",
            #         "margin": "0px",
            #         "--hover-color": "blue",
            #     },
            #     "nav-link-selected": {"background-color": "#02ab21"},
            # },
        )
    if "user_id" in st.session_state:
        print("STATE", st.session_state.user_id)
    if app == "Home":
        home.run()
    elif app == "Account":
        account.run()
    elif app == "Modules":
        modules.run()
    elif app == "Exercises":
        exercises.run()
    elif app == "About us":
        about.run()


if __name__ == "__main__":
    main()
