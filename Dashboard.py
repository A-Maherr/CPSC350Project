# import streamlit as st
# import time
# import pandas as pd

# conn = st.connection('dataset_db', type='sql')

# def dashboard_page():
#     st.title ("Dashboard")
#     st.write(f"Welcome to your dashboard, {st.session_state.username}!")
#     st.columns(1) 
#     if st.button("Input Data", key="input_data_button"):
#         st.session_state.page = "datainput_month"
#         st.rerun()

# Dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# connect to the same DB name you use elsewhere
conn = st.connection('dataset_db', type='sql')

def get_available_months_for_user(user_id):
    """
    Returns a sorted list of distinct YYYY-MM strings where the user has either income or expense data.
    """
    q = f"""
    SELECT DISTINCT date FROM (
        SELECT date FROM Income WHERE user_id = {user_id}
        UNION
        SELECT date FROM Expenses WHERE user_id = {user_id}
    )
    ORDER BY date;
    """
    try:
        df = conn.query(q)
        if df is None or df.empty:
            return []
        # data returned as a DF with column 'date'
        return [row['date'] for row in df.to_dict(orient='records')]
    except Exception as e:
        st.error(f"Error reading months from DB: {e}")
        return []

def get_earliest_month_for_user(user_id):
    q = f"""
    SELECT MIN(date) as min_date FROM (
        SELECT date FROM Income WHERE user_id = {user_id}
        UNION
        SELECT date FROM Expenses WHERE user_id = {user_id}
    );
    """
    try:
        df = conn.query(q)
        if df is None or df.empty:
            return None
        val = df.iloc[0].get('min_date') if 'min_date' in df.columns else df.iloc[0].get('MIN(date)')
        return val
    except Exception as e:
        st.error(f"Error reading earliest month: {e}")
        return None

def query_income(user_id, start_month, end_month):
    q = f"""
    SELECT date, monthly_income
    FROM Income
    WHERE user_id = {user_id}
    AND date BETWEEN '{start_month}' AND '{end_month}'
    ORDER BY date;
    """
    try:
        df = conn.query(q)
        if df is None:
            return pd.DataFrame(columns=['date', 'monthly_income'])
        return pd.DataFrame(df)
    except Exception as e:
        st.error(f"Error querying income: {e}")
        return pd.DataFrame(columns=['date', 'monthly_income'])

def query_expenses_by_category(user_id, start_month, end_month):
    q = f"""
    SELECT et.name AS category, SUM(e.amount) AS total
    FROM Expenses e
    JOIN Expense_type et ON e.type_id = et.id
    WHERE e.user_id = {user_id}
      AND e.date BETWEEN '{start_month}' AND '{end_month}'
    GROUP BY et.name
    ORDER BY total DESC;
    """
    try:
        df = conn.query(q)
        if df is None:
            return pd.DataFrame(columns=['category', 'total'])
        return pd.DataFrame(df)
    except Exception as e:
        st.error(f"Error querying expenses: {e}")
        return pd.DataFrame(columns=['category', 'total'])

def dashboard_page():
    st.title("Dashboard")
    username = st.session_state.get("username", "User")
    st.write(f"Welcome to your dashboard, {username}!")

    # Ensure user_id exists in session
    if "user_id" not in st.session_state:
        st.warning("No user logged in. Please log in first.")
        return

    user_id = st.session_state.user_id

    # Determine available months and earliest month in DB for this user
    months = get_available_months_for_user(user_id)
    earliest_month = get_earliest_month_for_user(user_id)

    if not months:
        st.info("No data found for your account yet. Click 'Input Data' to add your first month.")
        if st.button("Input Data"):
            st.session_state.page = "datainput_month"
            st.rerun()
        return

    # default end = current month in YYYY-MM
    current_month = datetime.now().strftime("%Y-%m")
    if current_month not in months:
        # ensure present in options (if current month has no data, keep current as default end,
        # but users should only be able to select actual months; so we clamp default to latest available month)
        default_end = months[-1]
    else:
        default_end = current_month

    # default start = earliest month (per your request)
    default_start = earliest_month if earliest_month else months[0]

    # Side-by-side month pickers implemented as selectboxes of available months
    c1, c2, c3 = st.columns([4,4,2])
    with c1:
        start_month = st.selectbox("From (month)", months, index=months.index(default_start) if default_start in months else 0, key="dash_start_month")
    with c2:
        end_month = st.selectbox("To (month)", months, index=months.index(default_end) if default_end in months else len(months)-1, key="dash_end_month")
    with c3:
        apply = st.button("Apply Filter", key="dash_apply_filter")

    # Validate range consistency whenever user presses Apply
    if apply:
        # Ensure start is not earlier than earliest_month (should be guaranteed by selectbox but double-check)
        if earliest_month and start_month < earliest_month:
            st.error(f"Selected start month ({start_month}) is earlier than earliest data month ({earliest_month}). Please pick a valid start month.")
        elif start_month > end_month:
            st.error("Start month must be earlier than or equal to end month.")
        else:
            st.session_state.dash_start_month = start_month
            st.session_state.dash_end_month = end_month

    # If the user hasn't applied filter yet, use defaults stored in session or computed defaults
    dash_start = st.session_state.get("dash_start_month", default_start)
    dash_end = st.session_state.get("dash_end_month", default_end)

    st.markdown(f"**Showing data from:** {dash_start}  →  **to:** {dash_end}")

    # Query data
    income_df = query_income(user_id, dash_start, dash_end)
    expenses_df = query_expenses_by_category(user_id, dash_start, dash_end)

    # KPIs: only if we have sufficient data
    total_income = 0.0
    total_expenses = 0.0

    if not income_df.empty:
        # Ensure numeric type
        income_df['monthly_income'] = pd.to_numeric(income_df['monthly_income'], errors='coerce')
        total_income = income_df['monthly_income'].sum()

    if not expenses_df.empty:
        expenses_df['total'] = pd.to_numeric(expenses_df['total'], errors='coerce')
        total_expenses = expenses_df['total'].sum()

    remainder = total_income - total_expenses

    # Show KPIs only if at least one of income or expenses exists (per your rule: show only when required data exists)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Remainder", f"${remainder:,.2f}")

    # Charts row
    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)

    # Income line chart (only show if income data exists in the selected range)
    if not income_df.empty:
        # prepare timeseries, set index to date
        income_ts = income_df.copy()
        if 'date' in income_ts.columns:
            income_ts = income_ts[['date', 'monthly_income']].set_index('date')
            income_ts.index = pd.to_datetime(income_ts.index.astype(str)) 
        chart_col1.subheader("Income over time")
        try:
            chart_col1.line_chart(income_ts['monthly_income'])
        except Exception as e:
            chart_col1.error(f"Unable to draw income chart: {e}")
    else:
        chart_col1.info("No income data found for the selected range. Income chart will appear once income data exists in range.")


    st.markdown("---")
    # Navigation button to go to the input flow
    btn_col1, btn_col2 = st.columns([1,5])
    with btn_col2:
        if st.button("Input Data"):
            st.session_state.page = "datainput_month"
            st.rerun()

# If this file is run directly by Streamlit, render the page:
if __name__ == "__main__":
    dashboard_page()
