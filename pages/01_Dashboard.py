import streamlit as st
import io
import json
from services.ai_service import ai_help
import pandas as pd
import time
from components.upload import show_upload
from services.data_loader import load_dataframe
from components.footer import show_footer

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

df = st.session_state.main_df

st.header("Dataset Summary", text_alignment="center")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Column Types")
    with st.container(border=True):
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
    
    
    # st.text(buffer.getvalue())

with col2:
    st.subheader("AI Suggested Column Types")

    sample = df.head(20).to_csv(index=False)
    prompt1 = f"""
        Analyze the dataset sample below and infer the most appropriate pandas datatype
        for every column.

        Allowed datatypes:
        - int64
        - float64
        - string
        - bool
        - datetime64[ns]
        - category

        Return ONLY a valid JSON object.
        Do not include explanations.
        Do not use markdown.
        Do not use ```json.

        Dataset sample:
        {sample}
        """

    ai_df = df.copy()
    ai_response = ai_help(prompt1)
    # st.text(ai_response) #debug
    dtype_map = json.loads(ai_response)

    for col, dtype in dtype_map.items():
        try:
            if dtype == "datetime64[ns]":
                ai_df[col] = pd.to_datetime(ai_df[col], errors="coerce")

            elif dtype in ["int64", "float64"]:
                ai_df[col] = pd.to_numeric(ai_df[col], errors="coerce")

                if dtype == "int64":
                    ai_df[col] = ai_df[col].astype("Int64")  # nullable integer

            else:
                ai_df[col] = ai_df[col].astype(dtype)

        except Exception as e:
            st.error(f"{col}: {e}")
    buffer = io.StringIO()
    ai_df.info(buf=buffer)
    st.text(buffer.getvalue())
    

if st.button("Continue with AI suggested Column types."):
    df = ai_df

st.write(df.describe())

# if st.button("Start the magic🪄 — Click Me!"):
# st.header("here birador")
prompt2 = f"""
    Dataset columns: {list(df.columns)}
    Data types: {df.dtypes.astype(str).to_dict()}

    Analyze this dataset and identify the 5 most important business KPIs.

    Return ONLY valid JSON in this format:

    [
        {{
            "name": "Average Salary",
            "column": "salary",
            "aggregation": "mean"
        }},
        {{
            "name": "Total Employees",
            "column": "employee_id",
            "aggregation": "count"
        }}
    ]

    Allowed aggregations:
    count
    sum
    mean
    median
    max
    min
    nunique

    Do not return Python code.
    Do not return explanations.
    Return only JSON.
    """
kpis = json.loads(ai_help(prompt2))

st.subheader("Key Dataset Metrics:")

for kpi in kpis:
    col = kpi["column"]
    agg = kpi["aggregation"]

    if agg == "mean":
        value = df[col].mean()
    elif agg == "sum":
        value = df[col].sum()
    elif agg == "count":
        value = df[col].count()
    elif agg == "nunique":
        value = df[col].nunique()

    if isinstance(value, (int, float)):
        value = round(value, 2)
    
    st.metric(kpi["name"], value)
        # data = ai_help(prompt2)

# -------------------------------------------------------------------------------------------
# st.snow()
st.subheader("Column vs Missing Values:")
missing = df.isnull().sum()
st.bar_chart(missing[missing > 0], y_label= "Missing Values")
numeric_cols = df.select_dtypes(include="number").columns
# if numeric_cols:

# =============bar chart ends============================

corr = df.select_dtypes(include="number").corr()
summary = df.describe(include="all").to_string()

insights = ai_help(
    f"Analyze this dataset summary and provide 5 business insights:\n{summary}"
)
st.subheader("Business Insights:")
st.write(insights)

show_footer()