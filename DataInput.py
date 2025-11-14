import streamlit as st
from datetime import datetime
from streamlit_date_picker import date_picker, PickerType
import time
from sqlalchemy import text


def page_month():
    st.title("Data Input - Select Month")
    selected_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="month_picker"
            ) 
    if st.button("Next "):
        st.session_state.selected_month = selected_month
        st.session_state.page = "datainput_income"
        st.rerun()

def page_income():
    canProceed = False
    st.title(f"Data Input - Enter Income for the month {st.session_state.selected_month}")
    income = st.text_input("Total Monthly Income", placeholder=f"e.g., your total income for the month ", key="income_input")
    if income:
        if check_input(income): 
            canProceed = True
            st.session_state.user_income = income 

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "datainput_month"
            st.rerun()
    with col2:
        if canProceed:
            if st.button("Next"):
                st.session_state.user_income = income
                st.session_state.page = "datainput_expenses"
                st.rerun()


def page_expenses():
    canProceed = False
    st.title(f"Data Input - Enter Expenses for the month {st.session_state.selected_month}")
    st.session_state.ValidationCounter = 0
    Housing = st.text_input("Housing", placeholder="e.g., monthly rent or mortgage payment", key="rent_input")
    if Housing: 
        if check_input(Housing):   st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    transportation = st.text_input("Transportation", placeholder="e.g., gas, public transit, rideshare", key="transportation_input")
    if transportation: 
        if check_input(transportation): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    groceries = st.text_input("Groceries", placeholder="e.g., food, household supplies", key="groceries_input")
    if groceries: 
        if check_input(groceries): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    utilities = st.text_input("Utilities", placeholder="e.g., electricity, water, internet", key="utilities_input")
    if utilities:  
        if check_input(utilities): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    Clothing = st.text_input("Clothing", placeholder="e.g., apparel, shoes, accessories", key="clothing_input")
    if Clothing: 
        if check_input(Clothing): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    Healthcare = st.text_input("Healthcare", placeholder="e.g., medical bills, prescriptions, insurance", key="healthcare_input")
    if Healthcare: 
        if check_input(Healthcare): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    PersonalCare = st.text_input("Personal Care", placeholder="e.g., toiletries, grooming, wellness", key="personalcare_input")
    if PersonalCare: 
        if check_input(PersonalCare):st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    DebtPayments = st.text_input("Debt Payments", placeholder="e.g., credit card, student loan, personal loan", key="debtpayments_input")
    if DebtPayments: 
        if check_input(DebtPayments): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    Miscellaneous = st.text_input("Miscellaneous", placeholder="e.g., entertainment, dining out, subscriptions", key="miscellaneous_input")
    if Miscellaneous: 
        if check_input(Miscellaneous): st.session_state.ValidationCounter += 1
        else: st.session_state.ValidationCounter -= 1
    
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "datainput_income"
            st.rerun()
    with col2:
        if st.session_state.ValidationCounter == 9:
            if st.button("Next"):
                st.session_state.Housing = Housing
                st.session_state.Transportation = transportation
                st.session_state.Groceries = groceries
                st.session_state.Utilities = utilities
                st.session_state.Clothing = Clothing
                st.session_state.Healthcare = Healthcare
                st.session_state.PersonalCare = PersonalCare
                st.session_state.DebtPayments = DebtPayments
                st.session_state.Miscellaneous = Miscellaneous
                st.session_state.page = "datainput_summary"
                st.rerun()


def page_summary():
    st.title("Summary")
    st.write("Month:", st.session_state.get("selected_month"))
    st.write("Income:", st.session_state.get("user_income"))
    st.write("  Housing:", st.session_state.get("Housing"))
    st.write("  Transportation:", st.session_state.get("Transportation"))
    st.write("  Groceries:", st.session_state.get("Groceries"))
    st.write("  Utilities:", st.session_state.get("Utilities"))
    st.write("  Clothing:", st.session_state.get("Clothing"))
    st.write("  Healthcare:", st.session_state.get("Healthcare"))
    st.write("  Personal Care:", st.session_state.get("PersonalCare"))
    st.write("  Debt Payments:", st.session_state.get("DebtPayments"))
    st.write("  Miscellaneous:", st.session_state.get("Miscellaneous"))

    if st.button("Start Over"):
        st.session_state.page = "datainput_month"
        st.rerun()
    if st.button("Submit"):
        conn = st.connection('dataset_db', type='sql') 
        income_insertion = text(f"INSERT INTO Income (user_id, monthly_income, date) VALUES ({st.session_state.user_id}, {st.session_state.user_income}, '{st.session_state.selected_month}');")
        Housing_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 1, {st.session_state.Housing}, '{st.session_state.selected_month}');")
        Transportation_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 2, {st.session_state.Transportation}, '{st.session_state.selected_month}');")
        Groceries_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 3, {st.session_state.Groceries}, '{st.session_state.selected_month}');")
        Utilities_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 4, {st.session_state.Utilities}, '{st.session_state.selected_month}');")
        Clothing_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 5, {st.session_state.Clothing}, '{st.session_state.selected_month}');")
        Healthcare_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 6, {st.session_state.Healthcare}, '{st.session_state.selected_month}');")
        PersonalCare_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 7, {st.session_state.PersonalCare}, '{st.session_state.selected_month}');")
        DebtPayments_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 8, {st.session_state.DebtPayments}, '{st.session_state.selected_month}');")
        Miscellaneous_insertion = text(f"INSERT INTO Expenses (user_id, type_id, amount, date) VALUES ({st.session_state.user_id}, 9, {st.session_state.Miscellaneous}, '{st.session_state.selected_month}');")

        with conn.session as s:
            if float(st.session_state.user_income) > 0:
                s.execute(income_insertion)
            if float(st.session_state.Housing) > 0:
                s.execute(Housing_insertion)
            if float(st.session_state.Transportation) > 0:
                s.execute(Transportation_insertion)
            if float(st.session_state.Groceries) > 0:
                s.execute(Groceries_insertion)
            if float(st.session_state.Utilities) > 0:
                s.execute(Utilities_insertion)
            if float(st.session_state.Clothing) > 0:
                s.execute(Clothing_insertion)
            if float(st.session_state.Healthcare) > 0:
                s.execute(Healthcare_insertion)
            if float(st.session_state.PersonalCare) > 0:
                s.execute(PersonalCare_insertion)
            if float(st.session_state.DebtPayments) > 0:
                s.execute(DebtPayments_insertion)
            if float(st.session_state.Miscellaneous) > 0:
                s.execute(Miscellaneous_insertion)
            s.commit()

        st.success("Data submitted successfully!")
        time.sleep(2)
        st.session_state.page = "dashboard"
        st.rerun()

def check_input(input):
    try:
        float(input)
        return True
    except ValueError:
        st.session_state.ValidationCounter -= 1
        st.error("Please enter a valid number.")
        return False
    