import streamlit as st

def show_upload():
    uploaded = st.file_uploader("Please upload your csv file.", type=["csv", "xlsx", "txt"])
    return uploaded