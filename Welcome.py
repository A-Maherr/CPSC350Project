import streamlit as st
from LogIn import login_page
from CreateAccount import create_account_page
from Dashboard import dashboard_page
from DataInput import page_month, page_income, page_expenses, page_summary

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()

if st.session_state.page == "create_account":
    create_account_page()

if st.session_state.page == "datainput_month":
    page_month()

if st.session_state.page == "datainput_income":
    page_income()

if st.session_state.page == "datainput_expenses":
    page_expenses()

if st.session_state.page == "datainput_summary":
    page_summary()

if st.session_state.page == "dashboard":
    dashboard_page()
