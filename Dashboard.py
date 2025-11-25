# Stacked-bar chart, expenses vs income for each month
# Stacked-bar chart, categories vs expenses per month. So each category is on the X axis and has the total spending for that category in the selected time period,
# split by how much you spent on that category each month, creating a select box for each category. So not all the categories are on one X-Y axis but the user gets
# to pick which category to display
# Pie-chart / Cirlce Chart of some sort for the savings/remainder page nivo.pie https://discuss.streamlit.io/t/streamlit-elements-issue-pie-chart-tooltip-text-color-not-showing-in-dark-mode/53072

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from sqlalchemy import text
from streamlit_elements import elements, nivo 
from streamlit_date_picker import date_picker, PickerType

# ---------------------------------------------------------
# CATEGORY MAP
# ---------------------------------------------------------
CATEGORY_MAP = {
    1:"Housing", 
    2:"Transportation", 
    3:"Groceries", 
    4:"Utilities",
    5:"Clothing", 
    6:"Healthcare", 
    7:"PersonalCare", 
    8:"DebtPayments", 
    9:"Miscellaneous"
}

conn = st.connection('dataset_db', type='sql')

# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------
def dashboard_page():

    st.title("📊 Dashboard Overview")

    # ---------------------------------------------------------
    # DATE RANGE PICKERS (return "YYYY-MM")
    # ---------------------------------------------------------
    colA, colB = st.columns(2)

    with colA:
        start_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="dash_start_month"
        )

    with colB:
        end_month = date_picker(
            picker_type=PickerType.month,
            value=datetime.now(),
            key="dash_end_month"
        )

    # -------------------------------------------------------------------
    # Validate that the returned picker value is a string
    # It will be like "2025-11"
    # -------------------------------------------------------------------
    if isinstance(start_month, datetime):
        start_month = start_month.strftime("%Y-%m")

    if isinstance(end_month, datetime):
        end_month = end_month.strftime("%Y-%m")

    # Guarantee correct string form
    start_month = str(start_month)
    end_month = str(end_month)

    # -------------------------------------------------------------------
    # Query database
    # -------------------------------------------------------------------

    inc_query = f" SELECT date, monthly_income FROM Income WHERE user_id = {st.session_state.user_id} AND date >= '{start_month}'  AND date <= '{end_month}' ORDER BY date; "

    exp_query = f" SELECT date, type_id, amount FROM Expenses WHERE user_id = {st.session_state.user_id} AND date >= '{start_month}' AND date <= '{end_month}' ORDER BY date; "

    income_df = conn.query(inc_query, ttl=0)
    expense_df = conn.query(exp_query, ttl=0)

    # -------------------------------------------------------------------
    # KPI CARDS
    # -------------------------------------------------------------------
    total_income = float(income_df["monthly_income"].sum()) if not income_df.empty else 0
    total_expenses = float(expense_df["amount"].sum()) if not expense_df.empty else 0
    remainder = total_income - total_expenses

    st.markdown("### 📈 Summary Metrics")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Income", f"${total_income:,.2f}")
    c2.metric("Total Expenses", f"${total_expenses:,.2f}")
    c3.metric("Savings / Remainder", f"${remainder:,.2f}")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 1️⃣ Income Line Chart
    # -------------------------------------------------------------------
    st.subheader("Income Over Time")

    if not income_df.empty:
        income_df["date_dt"] = pd.to_datetime(income_df["date"], format="%Y-%m")

        chart_line = (
            alt.Chart(income_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("date_dt:T", title="Month"),
                y=alt.Y("monthly_income:Q", title="Income"),
                tooltip=["date", "monthly_income"]
            )
            .properties(height=300)
        )

        st.altair_chart(chart_line, use_container_width=True)
    else:
        st.info("No income data for the selected range.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 2️⃣ Stacked bar: Income vs Expenses
    # -------------------------------------------------------------------
    st.subheader("Income vs Total Monthly Expenses")

    if not expense_df.empty or not income_df.empty:

        # Aggregate expenses by month
        exp_month = expense_df.groupby("date")["amount"].sum().reset_index()

        # Merge income and expense
        merged = pd.merge(
            income_df.rename(columns={"monthly_income": "income"}),
            exp_month,
            on="date",
            how="outer"
        ).fillna(0)

        merged["date_dt"] = pd.to_datetime(merged["date"], format="%Y-%m")
        
        merged["income"] = pd.to_numeric(merged["income"], errors="coerce").fillna(0)
        merged["amount"] = pd.to_numeric(merged["amount"], errors="coerce").fillna(0)
        st.write("DEBUG dtype:", merged.dtypes)
        
        bar = (
            alt.Chart(merged)
            .transform_fold(
                ["income", "amount"],
                as_=["Type", "Value"]
            )
            .mark_bar()
            .encode(
                x=alt.X("date_dt:T", title="Month"),
                y=alt.Y("Value:Q", title="Amount", stack="zero"),
                color=alt.Color("Type:N", title="Category",
                                scale=alt.Scale(scheme="set2")),
                tooltip=[
                    alt.Tooltip("date:N", title="Month"),
                    alt.Tooltip("Type:N", title="Type"),
                    alt.Tooltip("Value:Q", title="Amount")
                ],
            )
            .properties(
                title="Income vs Expenses (Stacked)",
                height=350
            )
    )


        st.altair_chart(bar, use_container_width=True) 
    else:
        st.info("Not enough data to display.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 3️⃣ Category-by-month stacked chart (user controllable)
    # -------------------------------------------------------------------
    st.subheader("Category Spending by Month")
    if st.button("input data"):
        st.session_state.page = "datainput_month"
        st.rerun()
    category_list = list(CATEGORY_MAP.values())
    selected_cat = st.selectbox("Select category to view:", category_list)

    selected_type_id = [
        key for key, val in CATEGORY_MAP.items() if val == selected_cat
    ][0]

    subset = expense_df[expense_df["type_id"] == selected_type_id]

    if not subset.empty:
        cat_month = subset.groupby("date")["amount"].sum().reset_index()
        cat_month["date_dt"] = pd.to_datetime(cat_month["date"], format="%Y-%m")

        bar_cat = (
            alt.Chart(cat_month)
            .mark_bar()
            .encode(
                x=alt.X("date_dt:T", title="Month"),
                y=alt.Y("amount:Q", title=f"{selected_cat} Spending"),
                tooltip=["date", "amount"]
            )
            .properties(height=300)
        )

        st.altair_chart(bar_cat, use_container_width=True)
    else:
        st.info(f"No spending data for **{selected_cat}** in this date range.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 4️⃣ Savings / Remainder Pie Chart (Nivo)
    # -------------------------------------------------------------------
    st.subheader("Savings Distribution (Income vs Expenses vs Remainder)")

    pie_data = [
        {"id": "Income", "label": "Income", "value": total_income},
        {"id": "Expenses", "label": "Expenses", "value": total_expenses},
        {"id": "Savings", "label": "Savings", "value": remainder},
    ]

    with elements("pie_chart"):
        nivo.Pie(
            data=pie_data,
            margin=dict(top=40, right=80, bottom=80, left=80),
            innerRadius=0.4,
            padAngle=0.7,
            cornerRadius=3,
            activeOuterRadiusOffset=8,
            colors={"scheme": "paired"},
            borderWidth=1,
            borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
            arcLabel="value",
            arcLabelsTextColor="#ffffff",
            legends=[
                {
                    "anchor": "bottom",
                    "direction": "row",
                    "translateY": 56,
                    "itemWidth": 100,
                    "itemHeight": 18,
                    "symbolSize": 18,
                    "symbolShape": "circle",
                }
            ]
        )
