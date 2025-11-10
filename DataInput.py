import streamlit as st
from datetime import datetime
from streamlit_date_picker import date_picker, PickerType

def page_month():
    st.title("Step 1: Choose Month")
    selected_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="month_picker"
            ) 
    if st.button("Next "):
        st.session_state.month = selected_month
        st.session_state.page = "datainput_income"
        st.rerun()

def page_income():
    st.title("Step 2: Enter Income")
    income = st.number_input("Total income", min_value=0.0, step=100.0, key="income_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "datainput_month"
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.income = income
            st.session_state.page = "datainput_expenses"
            st.rerun()


def page_expenses():
    st.title("Step 3: Enter Expenses")
    rent = st.number_input("Rent", min_value=0.0, step=50.0, key="rent_input")
    food = st.number_input("Food", min_value=0.0, step=50.0, key="food_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "datainput_income"
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.expenses = {"rent": rent, "food": food}
            st.session_state.page = "datainput_summary"
            st.rerun()


def page_summary():
    st.title("Summary")
    st.write("Month:", st.session_state.get("month", "N/A"))
    st.write("Income:", st.session_state.get("income", "N/A"))
    st.write("Expenses:", st.session_state.get("expenses", {}))

    if st.button("Start Over"):
        st.session_state.page = "dashboard"
        st.rerun()
