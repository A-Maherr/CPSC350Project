import streamlit as st
import time
from LogIn import login_page
from CreateAccount import create_account_page

# Set page config
st.set_page_config(page_title="Welcome", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "login"
    
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "create_account":
    create_account_page()
