import json
from openai import OpenAI
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from streamlit_elements import elements, nivo
from streamlit_date_picker import date_picker, PickerType
from streamlit_elements import mui

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


def dashboard_page():
    
    st.title("Dashboard Overview", width="stretch")
    left, right = st.columns([4, 1])
    with left:
        st.markdown("### Time Range")
    with right:
        if st.button("➕ Add Data"):
            st.session_state.page = "datainput_month"
            st.rerun()

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

    
    if isinstance(start_month, datetime):
        start_month = start_month.strftime("%Y-%m")
    if isinstance(end_month, datetime):
        end_month = end_month.strftime("%Y-%m")

    start_month = str(start_month)
    end_month = str(end_month)

    inc_query = f"""
        SELECT date, monthly_income 
        FROM Income 
        WHERE user_id = {st.session_state.user_id}
        AND date >= '{start_month}'
        AND date <= '{end_month}'
        ORDER BY date;
    """

    exp_query = f"""
        SELECT date, type_id, amount 
        FROM Expenses 
        WHERE user_id = {st.session_state.user_id}
        AND date >= '{start_month}'
        AND date <= '{end_month}'
        ORDER BY date;
    """

    income_df = conn.query(inc_query, ttl=0)
    expense_df = conn.query(exp_query, ttl=0)

    total_income = float(income_df["monthly_income"].sum()) if not income_df.empty else 0
    total_expenses = float(expense_df["amount"].sum()) if not expense_df.empty else 0
    remainder = total_income - total_expenses

    st.markdown("### Summary Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Income", f"${total_income:,.2f}")
    k2.metric("Total Expenses", f"${total_expenses:,.2f}")
    k3.metric("Savings / Remainder", f"${remainder:,.2f}")


    total_income = float(income_df["monthly_income"].sum()) if not income_df.empty else 0

    total_expenses = float(expense_df["amount"].sum()) if not expense_df.empty else 0

    total_retained = total_income - total_expenses

    expense_df["category"] = expense_df["type_id"].map(CATEGORY_MAP)
    category_totals = (
        expense_df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )   

    monthly_retained = []
    if not income_df.empty:
        exp_month = expense_df.groupby("date")["amount"].sum().reset_index()
        merged_tmp = pd.merge(
            income_df.rename(columns={"monthly_income": "income"}),
            exp_month.rename(columns={"amount": "expenses"}),
            on="date",
            how="outer"
        ).fillna(0)
        merged_tmp["retained"] = merged_tmp["income"] - merged_tmp["expenses"]
        merged_tmp = merged_tmp.sort_values("date")
        monthly_retained = merged_tmp["retained"].tolist()

    ai_summary_data = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_retained": total_retained,
        "category_totals": category_totals,
        "monthly_retained": monthly_retained,   
    }

    client = OpenAI(api_key=st.secrets["API_KEY"])

    prompt = f"""
    You are a financial insights assistant. Generate ONE meaningful insight about
    the user's spending habits based on this summary. Keep it to 1–2 sentences.

    DATA SUMMARY (JSON):
    {json.dumps(ai_summary_data)}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_fact = response.choices[0].message.content
    st.subheader("AI Insight")

    st.info(ai_fact)
    st.subheader("Retained Income Over Time")

    exp_month = expense_df.groupby("date")["amount"].sum().reset_index()

    merged_retained = (
        pd.merge(
            income_df.rename(columns={"monthly_income": "income"}),
            exp_month.rename(columns={"amount": "expenses"}),
            on="date",
            how="outer"
        )
    )

    if merged_retained.empty:
        st.info("No data available in this time range.")
    else:
        merged_retained["date_dt"] = pd.to_datetime(merged_retained["date"], format="%Y-%m")

        merged_retained = merged_retained.dropna(subset=["income", "expenses"], how="all")

        merged_retained = merged_retained.fillna(0)

        if merged_retained.empty:
            st.info("Not enough data for the selected range")
        else:
            merged_retained = merged_retained.sort_values("date_dt")

            merged_retained["retained"] = merged_retained["income"] - merged_retained["expenses"]

            merged_retained["month_label"] = merged_retained["date_dt"].dt.strftime("%b %Y")

            if merged_retained["retained"].sum() == 0:
                st.info("Not enough data for the selected range.")
            else:
                line_chart = (
                    alt.Chart(merged_retained)
                    .mark_line(color="#4FC3F7", strokeWidth=3)
                    .encode(
                        x=alt.X(
                            "month_label:N",
                            title="Month",
                            sort=alt.SortField("date_dt", "ascending")
                        ),
                        y=alt.Y("retained:Q", title="Retained Income"),
                        tooltip=["month_label", "income", "expenses", "retained"]
                    )
                    .properties(height=350)
                )

                points = (
                    alt.Chart(merged_retained)
                    .mark_point(size=90, filled=True, color="#4FC3F7")
                    .encode(
                        x=alt.X("month_label:N", sort=alt.SortField("date_dt", "ascending")),
                        y="retained:Q"
                    )
                )

                st.altair_chart(line_chart + points, use_container_width=True)

    st.markdown("---")

# Income vs Monthly Expenses 

    st.subheader("Income vs Monthly Expenses")

    if not income_df.empty or not expense_df.empty:

        exp_month = expense_df.groupby("date")["amount"].sum().reset_index()

        merged = (
            pd.merge(
                income_df.rename(columns={"monthly_income": "Income"}),
                exp_month.rename(columns={"amount": "Expenses"}),
                on="date",
                how="outer"
            ).fillna(0)
        )

        merged["date_dt"] = pd.to_datetime(merged["date"], format="%Y-%m")
        merged = merged.sort_values("date_dt") 
        merged["month_label"] = merged["date_dt"].dt.strftime("%b %Y")

        melted = merged.melt(
            id_vars=["date_dt", "month_label"],
            value_vars=["Expenses", "Income"],
            var_name="Category",
            value_name="Value"
        )

        color_scale = alt.Scale(
            domain=["Expenses", "Income"],        
            range=["#EF5350", "#42A5F5"]       
        )

        bar = (
            alt.Chart(melted)
            .mark_bar(size=55)
            .encode(
                x=alt.X("month_label:N", title="Month",
                        sort=list(melted["month_label"].unique())),
                y=alt.Y("Value:Q", title="Amount", stack="zero"),
                color=alt.Color(
                    "Category:N",
                    scale=color_scale,
                    sort=["Expenses", "Income"], 
                    title="Category"
                ),
                tooltip=["month_label", "Category", "Value"]
            )
            .properties(height=380)
        )

        st.altair_chart(bar, use_container_width=True)

    else:
        st.info("Not enough data for the selected range.")

    st.markdown("---")

# Category Spending Breakdown 
    st.subheader("Category Spending Breakdown (Stacked by Month)")

    if not expense_df.empty:

        
        expense_df["category"] = expense_df["type_id"].map(CATEGORY_MAP)

        
        exp_cat_month = (
            expense_df.groupby(["category", "date"])["amount"]
            .sum()
            .reset_index()
        )

        
        exp_cat_month["date_dt"] = pd.to_datetime(exp_cat_month["date"], format="%Y-%m")
        exp_cat_month["month_label"] = exp_cat_month["date_dt"].dt.strftime("%b %Y")

        
        bar_cat = (
            alt.Chart(exp_cat_month)
            .mark_bar(size=40)  
            .encode(
                y=alt.Y(
                    "category:N",
                    title="Category",
                    sort=list(CATEGORY_MAP.values())
                ),
                x=alt.X(
                    "amount:Q",
                    title="Amount",
                    stack="zero"
                ),
                color=alt.Color(
                    "month_label:N",
                    title="Month",
                    scale=alt.Scale(scheme="blues"),
                    legend = None
                ),
                tooltip=["category", "month_label", "amount"]
            )
            .properties(
                height=500  
            )
        )

        st.altair_chart(bar_cat, use_container_width=True)

    else:
        st.info("No expenses found in the selected date range.")
    st.markdown("---")


# CATEGORY EXPENSE SPLIT (NIVO PIE CHART)
    st.subheader("Expense Breakdown by Category")

    if not expense_df.empty:

        expense_df["category"] = expense_df["type_id"].map(CATEGORY_MAP)

        exp_by_cat = (
            expense_df.groupby("category")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
        )

        pie_data = [
            {"id": row["category"], "label": row["category"], "value": float(row["amount"])}
            for _, row in exp_by_cat.iterrows()
        ]

        with elements("category_pie"):

            mui.Box(
                children=[
                    nivo.Pie(
                        data=pie_data,
                        margin=dict(top=50, right=120, bottom=90, left=120),
                        innerRadius=0.45,
                        padAngle=1.0,
                        cornerRadius=4,
                        activeOuterRadiusOffset=10,
                        colors={"scheme": "set3"},
                        borderWidth=1,
                        borderColor={"from": "color", "modifiers": [["darker", 0.3]]},
                        arcLabel="value",
                        arcLabelsTextColor="#000",
                        arcLinkLabelsTextColor="#FFFFFF",
                        arcLinkLabelsColor={"from": "color"},
                        height=520,
                        legends=[
                            {
                                "anchor": "bottom",
                                "direction": "row",
                                "translateY": 60,
                                "itemWidth": 120,
                                "itemHeight": 18,
                                "symbolSize": 18,
                                "symbolShape": "circle",
                            }
                        ],
                        theme={
                            "textColor": "#FFFFFF",  
                            "legends": {
                                "text": {"fill": "#FFFFFF"}  
                            },
                            "tooltip": {
                                "container": {
                                    "background": "#222222",
                                    "color": "#ffffff",
                                    "fontSize": 14
                                }
                            }
                        }
                    )
                ],
                sx={
                    "width": "100%",
                    "height": 600,
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center"
                }
            )

    else:
        st.info("Not enough data for the selected range.")




