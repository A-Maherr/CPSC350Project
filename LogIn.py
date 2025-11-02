import streamlit as st
import pandas as pd
import time 
conn = st.connection('dataset_db', type='sql')

def login_page():
    st.title("Log In")
    username = st.text_input("Username", placeholder="Enter your username")

    if(st.button("Log In", use_container_width=True, key = "login_button")):
        if(username):
            if not conn.query(f"SELECT * from users where username = '{username}';", ttl=0).empty:
                st.success(f"Welcome back, {username}!")
                time.sleep(2)
                st.session_state.username = username
                st.session_state.page = "main_app"
                st.rerun()
            else:
                st.error("Username not found. Please create an account.")
        else:
            st.error("Please enter your username to log in.")

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
