from services.data_loader import load_dataframe
from services.datatype_service import data_summ
from components.upload import show_upload
from components.footer import show_footer
from services.kpi_service import get_kpi
from services.ai_service import ai_help
import streamlit as st
import pandas as pd
import json
import time
import io




if "main_df" not in st.session_state:
    st.warning("Please upload your data")
    uploaded_file = show_upload()
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        uploaded_df = load_dataframe(uploaded_file)
        st.session_state.main_df = uploaded_df
        st.session_state.data_source = "csv"
        # the_df = st.session_state.main_df
        st.rerun()
    st.stop()

df = st.session_state.main_df

st.header("Dataset Summary", text_alignment="center")
if st.session_state.data_source != "database":
    data_summ()


# st.write(st.session_state.main_df.describe())

st.subheader("Summary Statistics")
st.dataframe(st.session_state.main_df.describe())

if st.button("Generate top 5 KPIs"):
    try:
        get_kpi(st.session_state.main_df)
    except:
        st.error("Data processing failed due to invalid column types. Try applying the AI-suggested column types or upload a correctly formatted CSV file.")

# -------------------------------------------------------------------------------------------
# st.snow()
missing = st.session_state.main_df.isnull().sum()
if missing.sum() > 0:
    st.subheader("Column vs Missing Values:")
    st.bar_chart(missing[missing > 0], y_label= "Missing Values")
    numeric_cols = st.session_state.main_df.select_dtypes(include="number").columns
# if numeric_cols:

# =============bar chart ends============================

corr = st.session_state.main_df.select_dtypes(include="number").corr()
summary = st.session_state.main_df.describe(include="all").to_string()

insights = ai_help(
    f"Analyze this dataset summary and provide 5 business insights:\n{summary}"
)
st.subheader("Business Insights:")
st.write(insights)

show_footer()