import streamlit as st
import pandas as pd
import time 
conn = st.connection('dataset_db', type='sql')

st.set_page_config(layout="wide")

def login_page():
    st.title("Log In")
    username = st.text_input("Username", placeholder="Enter your username")
    col1, col2 = st.columns([1, 1])
    with col1:
        login = st.button("Log In", use_container_width=True, key = "login_button")
    if(login):
        if(username):
            if not conn.query(f"SELECT * from users where username = '{username}';", ttl=0).empty:
                st.success(f"Welcome back, {username}!")
                time.sleep(2)
                st.session_state.username = username
                st.session_state.user_id = conn.query(f"SELECT id from users where username = '{username}';", ttl=0).iloc[0,0]
                st.session_state.page = "datainput_month"
                st.rerun()
            else:
                st.error("Username not found. Please create an account.")
        else:
            st.error("Please enter your username to log in.")

    with col2:
        create = st.button("Create Account", use_container_width=True)

    if create:
        st.session_state.page = "create_account"
        st.rerun()

    st.write("---")
    st.caption("Enter your username to log in or create an account.")
