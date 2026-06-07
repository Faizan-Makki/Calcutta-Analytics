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

uploaded_file = show_upload()

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
    uploaded_df = load_dataframe(uploaded_file)
    st.session_state.main_df = uploaded_df
    st.write(uploaded_df)

show_footer()