import streamlit as st
from components.upload import show_upload
from services.data_loader import load_dataframe
from components.footer import show_footer
from services.datatype_service import data_summ
from services.cleaning_service import missings, rem_dup, fill_miss, drop_cols, change_dtype, download_data


if "main_df" not in st.session_state:
    st.warning("Please upload your data")
    uploaded_file = show_upload()
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        uploaded_df = load_dataframe(uploaded_file)
        st.session_state.main_df = uploaded_df
        st.session_state.data_source = "csv"
        st.session_state.updated_cols = False
        #st.session_state.main_df = st.session_state.main_df
        st.rerun()
    st.stop()


st.header("Dataset Summary", text_alignment="center")
if st.session_state.updated_cols == False:
    data_summ()

st.subheader("Missing Values")
missings()

st.subheader("Fill missings")
fill_miss()

if st.session_state.main_df.duplicated().sum() > 0:
    st.subheader("Remove duplicates")
    rem_dup()

st.subheader("Drop column")
drop_cols()

st.subheader("Change datatype")
change_dtype()

st.subheader("Download clean data")
download_data()

show_footer()