import streamlit as st
import pandas as pd

conn = st.connection('dataset_db', type='sql') 
expense_type = conn.query('SELECT * FROM expense_type')
st.dataframe(expense_type)