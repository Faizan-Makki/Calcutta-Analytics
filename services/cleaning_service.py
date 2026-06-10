import streamlit as st
import pandas as pd

def missings():
    missing = st.session_state.main_df.isnull().sum()
    st.dataframe(missing[missing > 0])


def rem_dup():
    duplicates = st.session_state.main_df.duplicated().sum()
    st.metric("Duplicate Rows", duplicates)
    if st.button("Remove Duplicates"):
        st.session_state.main_df = st.session_state.main_df.drop_duplicates()
        st.success("Duplicates removed.")


def fill_miss():
    numeric_cols = st.session_state.main_df.select_dtypes(include="number").columns
    col = st.selectbox("Select Numeric Column", numeric_cols)
    col1, col2, col3 = st.columns(3)
    with col1:
        mean_btn = st.button("Fill Missing with Mean")
    with col2:
        median_btn = st.button("Fill Missing with Median")
    with col3:
        mode_btn = st.button("Fill Missing with Mode")
    if mean_btn:
        mean_value = round(st.session_state.main_df[col].mean(), 0)
        st.session_state.main_df[col] = (
            st.session_state.main_df[col].fillna(mean_value)
        )
        st.success(
            f"Filled missing values in '{col}' with mean: {mean_value}"
        )
    elif median_btn:
        median_value = round(st.session_state.main_df[col].median(), 0)
        st.session_state.main_df[col] = (
            st.session_state.main_df[col].fillna(median_value)
        )

        st.success(
            f"Filled missing values in '{col}' with median: {median_value}"
        )

    elif mode_btn:
        mode_value = round(st.session_state.main_df[col].mode().iloc[0], 0)

        st.session_state.main_df[col] = (
            st.session_state.main_df[col].fillna(mode_value)
        )

        st.success(
            f"Filled missing values in '{col}' with mode: {mode_value}"
        )


def drop_cols():
    cols_to_drop = st.multiselect(
    "Select Columns to Drop",
   st.session_state.main_df.columns
    )
    if st.button("Drop Columns"):
        st.session_state.main_df =st.session_state.main_df.drop(columns=cols_to_drop)
        st.success(f"{cols_to_drop} dropped.")


def change_dtype():
    col = st.selectbox(
    "Select Column",
    st.session_state.main_df.columns
    )
    dtype = st.selectbox(
    "Convert To",
    ["int", "float", "str", "datetime"]
    )
    if st.button("Convert Datatype"):
        try:
            if dtype == "int":
                st.session_state.main_df[col] =st.session_state.main_df[col].astype("Int64")
            elif dtype == "float":
                st.session_state.main_df[col] =st.session_state.main_df[col].astype(float)
            elif dtype == "str":
                st.session_state.main_df[col] =st.session_state.main_df[col].astype(str)
            elif dtype == "datetime":
                st.session_state.main_df[col] = pd.to_datetime(st.session_state.main_df[col], errors="coerce")
            st.session_state.main_df = st.session_state.main_df
            st.success(f"{col} converted to {dtype}")
        except Exception as e:
            st.error(f"Conversion failed: {e}")


def download_data():
    st.dataframe(st.session_state.main_df.head())
    csv =st.session_state.main_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Cleaned CSV",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )