import streamlit as st
import time
import pandas as pd

conn = st.connection('dataset_db', type='sql')

def dashboard_page():
    st.title ("Dashboard")
    st.write(f"Welcome to your dashboard, {st.session_state.username}!")
    st.columns(1) 