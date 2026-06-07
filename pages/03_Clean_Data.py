import streamlit as st
from components.upload import show_upload
from services.data_loader import load_dataframe
import pandas as pd
from components.footer import show_footer

# if uploaded_file:
#     st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
#     uploaded_df = load_dataframe(uploaded_file)
#     st.session_state.main_df = uploaded_df




if "main_df" not in st.session_state:
    st.warning("Please upload your data")
    uploaded_file = show_upload()
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        uploaded_df = load_dataframe(uploaded_file)
        st.session_state.main_df = uploaded_df
        # the_df = st.session_state.main_df
        st.rerun()
    st.stop()
the_df = st.session_state.main_df
    

st.subheader("Missing Values")
missing = the_df.isnull().sum()
st.dataframe(missing[missing > 0])


st.subheader("Remove duplicates")
duplicates = the_df.duplicated().sum()
st.metric("Duplicate Rows", duplicates)
if st.button("Remove Duplicates"):
    st.session_state.main_df = st.session_state.main_df.drop_duplicates()
    the_df = st.session_state.main_df
    st.success("Duplicates removed.")


st.subheader("Fill missings")
numeric_cols = the_df.select_dtypes(include="number").columns
col = st.selectbox("Select Numeric Column", numeric_cols)

if st.button("Fill Missing with Mean"):
    mean_value = the_df[col].mean()
    the_df[col].fillna(round(the_df[col].mean(), 0), inplace=True)
    st.success(f"Filled missing {col} with average {col}: {round(st.session_state.main_df[col].mean(),0)}")
    missing = the_df.isnull().sum()
    st.dataframe(missing[missing > 0])

# Drop cols
st.subheader("Drop column")
cols_to_drop = st.multiselect(
    "Select Columns to Drop",
    the_df.columns
)

if st.button("Drop Columns"):
    the_df = the_df.drop(columns=cols_to_drop)
    st.success(f"{cols_to_drop} dropped.")
st.subheader("Change datatype")
col = st.selectbox(
"Select Column",
the_df.columns
)

dtype = st.selectbox(
    "Convert To",
    ["int", "float", "str", "datetime"]
)
if st.button("Convert Datatype"):
    try:
        if dtype == "int":
            the_df[col] = the_df[col].astype("Int64")
        elif dtype == "float":
            the_df[col] = the_df[col].astype(float)
        elif dtype == "str":
            the_df[col] = the_df[col].astype(str)
        elif dtype == "datetime":
            the_df[col] = pd.to_datetime(the_df[col], errors="coerce")

        st.session_state.main_df = the_df
        st.success(f"{col} converted to {dtype}")
    except Exception as e:
        st.error(f"Conversion failed: {e}")

csv = the_df.to_csv(index=False)

st.subheader("Download clean data")
st.download_button(
    "Download Cleaned CSV",
    csv,
    "cleaned_data.csv",
    "text/csv"
)

show_footer()