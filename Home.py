import streamlit as st
from components.header import show_header
from components.footer import show_footer
from components.upload import show_upload
from services.data_loader import load_dataframe
import pandas as pd

st.set_page_config(
    page_title="CALCUTTA ANALYTICS",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

show_header()
st.divider()
st.markdown("""
# Turn Raw Data Into Business Intelligence

Calcutta Analytics is an AI-powered analytics platform that helps analysts,
students, founders, and business teams transform raw datasets into actionable insights.


""")
st.subheader("Upload your dataset and instantly", text_alignment="center")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    📊 **AI KPI Discovery**

    Automatically identifies the most important
    business metrics in your dataset.
    """)

with col2:
    st.info("""
    🤖 **AI Data Copilot**

    Ask questions about your data
    using natural language.
    """)

col3, col4 = st.columns(2)

with col3:
    st.info("""
    🧹 **Data Quality Center**

    Detect missing values, duplicates,
    and datatype issues instantly.
    """)

with col4:
    st.info("""
    ⚡ **Code Studio**

    Generate Pandas code directly
    from plain English requests.
    """)


st.divider()
st.subheader("📂 Upload Dataset")
uploaded_file = show_upload()
st.subheader("or")
if st.button("Connect to database"):
    st.switch_page("pages/05_Database.py")
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
    uploaded_df = load_dataframe(uploaded_file)
    st.session_state.main_df = uploaded_df
    st.session_state.data_source = "csv"
    st.session_state.updated_cols = False
    st.switch_page("pages/01_Dashboard.py")
    # st.write(uploaded_df)

st.divider()

st.subheader("⚡ Analytics Workflow")

st.markdown("""
**1. Load Your Data**  
Upload CSV, Excel, or TXT files, or connect directly to your SQL database.

**2. Clean Data**  
Fix missing values, duplicates and datatypes.

**3. Generate Insights**  
Discover trends, KPIs and opportunities.

**4. Ask AI**  
Query your data using natural language.

**5. Export Results**  
Download cleaned datasets and outputs.
""")

show_footer()