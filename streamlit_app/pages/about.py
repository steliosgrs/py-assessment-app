import streamlit as st
import streamlit.components.v1 as components


def run():
    st.subheader("PyCamp is a website created for students to")
    st.subheader("study and learn Python.")
    st.markdown(
        "Created by: [Stelios Georgaras](https://github.com/steliosgrs) for [IEEE SB UniWa](https://github.com/ieee-sb-uniwa)"
    )
    st.markdown("Contact via mail: [steliosgp13@gmail.com]")

    st.link_button(
        "Συμπληρώστε την φόρμα ενδιαφέροντος",
        url="https://docs.google.com/forms/d/1UhNbqv-xMMryFgzw7P2nJNcml3vVMXNrBLxa2R3AXd4",
    )
