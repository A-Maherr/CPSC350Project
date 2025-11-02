import streamlit as st

def login_page():
    st.title("Log In")

    username = st.text_input("Username", placeholder="Enter your username")

    col1, col2 = st.columns([1, 1])
    with col1:
        login = st.button("Log In", use_container_width=True)
    with col2:
        create = st.button("Create Account", use_container_width=True)

    if create:
        st.session_state.page = "create_account"
        st.rerun()

    st.write("---")
    st.caption("Enter your username to log in or create an account.")
