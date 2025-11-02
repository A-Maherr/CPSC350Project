import streamlit as st
from sqlalchemy import text
import pandas as pd
import time 

conn = st.connection('dataset_db', type='sql') 

def create_account_page():
    st.title("Create Account")

    new_username = st.text_input("Choose a Username", placeholder="Enter a new username")
    
    if st.button("Sign Up", use_container_width=True):
        if(new_username):
            if conn.query(f"SELECT * from users where username = '{new_username}';", ttl=0).empty:
                insertion = f"INSERT INTO users (username) VALUES ('{new_username}');"
                insertion = text(insertion)
                s = conn.session
                s.execute (insertion, {"username": new_username})
                s.commit()
                st.success(f"Account created for {new_username}!")
                time.sleep(2)
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username already exists. Please choose a different username.")
        else:
            st.error("Please enter in your username to create an account")

    if st.button("Back to Login", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
