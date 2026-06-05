# =============================================================================
# STREAMLIT BASICS - All Core Concepts Covered
# Run with: streamlit run streamlit_basics.py
# Install with: pip install streamlit
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import time
from apiconfig import ai_help
import ast
import json
import io
# from analytics import uploaded_df, csv_file,total_orders,avg_ov, avg_can, ord_del, ret_rate
# st.image(
#     "Gemini_Generated_Image_bhb0khbhb0khbhb0.png",
#     width=100
# )
# st.title("CALCUTTA CONSULTING GROUP", text_alignment="center")
# st.title("")
# st.image(
#     "Gemini_Generated_Image_7k58967k58967k58.png",
#     use_container_width=True
# )

# csv_file = "orders.csv"
# uploaded_df = pd.read_csv(csv_file)

# =============================================================================
# 1. PAGE CONFIGURATION (must be the first Streamlit command)
# =============================================================================

st.set_page_config(
    page_title="Calcutta Consulting Group",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS to elevate UI styling (Hiding standard Streamlit clutter & setting typography)
st.markdown("""
    <style>
        /* Hide default Streamlit header and footer padding */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Corporate Title Styling */
        .corporate-title {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-weight: 700;
            color: #ffffff;
            font-size: 2.8rem;
            letter-spacing: -0.03em;
            margin: 0;
            line-height: 1.2;
        }
        
        /* Subtitle / Tagline Styling */
        .corporate-tagline {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #a3a3a3;
            font-size: 1.1rem;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }
        
        /* Hero Image Container to give it a clean border radius */
        .hero-container img {
            border-radius: 12px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Professional Header Section (Logo on left, Title text beautifully aligned beside it)
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    # Replace '9251755389922777815.jpeg' with your local logo path if needed
    st.image("media/logo.png", width=120)

with header_col2:
    st.markdown('<h1 class="corporate-title">CALCUTTA CONSULTING GROUP</h1>', unsafe_allow_html=True)
    st.markdown('<p class="corporate-tagline">Strategy. Analytics. Transformation.</p>', unsafe_allow_html=True)

# Clean structural divider
st.markdown("---")

# 4. Main Hero Image Section
# Replace 'watermarked_img_14851377396885550443.png' with your preferred local home background image path
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.image("media/main.png", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# =============================================================================
# 2. TEXT ELEMENTS
# =============================================================================
uploaded = st.file_uploader("Please upload your csv file.", type=["csv", "xlsx", "txt"])
if uploaded:
    st.success(f"Uploaded: {uploaded.name} ({uploaded.size} bytes)")
    uploaded_df = pd.read_csv(uploaded)

    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Ask AI","Generate pandas code","Clean Data"])
    with tab1:
        st.write(uploaded_df)
        st.header("Dataset Summary")
        st.markdown("#### Column Types & Counts:")
        buffer = io.StringIO()
        uploaded_df.info(buf=buffer)
        st.text(buffer.getvalue())

        # =============================================================
        st.markdown("#### AI Suggested Column Types & Counts:")

        sample = uploaded_df.head(20).to_csv(index=False)
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

        ai_df = uploaded_df.copy()
        ai_response = ai_help(prompt1)
        st.text(ai_response) #debug
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

        # ==========================================================

        if "main_df" not in st.session_state:
            st.session_state.main_df = uploaded_df

        if st.button("Continue with AI suggested Column types."):
            st.session_state.main_df = ai_df

        st.write(st.session_state.main_df.describe())

        if st.button("Start the magic🪄 — Click Me!"):
            st.header("here birador")
            main_df = st.session_state.main_df
            prompt2 = f"""
                Dataset columns: {list(main_df.columns)}
                Data types: {main_df.dtypes.astype(str).to_dict()}

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
                    value = main_df[col].mean()
                elif agg == "sum":
                    value = main_df[col].sum()
                elif agg == "count":
                    value = main_df[col].count()
                elif agg == "nunique":
                    value = main_df[col].nunique()

                if isinstance(value, (int, float)):
                    value = round(value, 2)
                
                st.metric(kpi["name"], value)
                    # data = ai_help(prompt2)

            # ================rejected=====================================

            # Generic KPIs
            # total_rows = len(st.session_state.main_df)
            # total_columns = len(st.session_state.main_df.columns)
            # missing_values = int(st.session_state.main_df.isna().sum().sum())

            # numeric_cols = st.session_state.main_df.select_dtypes(include="number").columns

            # if len(numeric_cols) > 0:
            #     avg_numeric = round(st.session_state.main_df[numeric_cols[0]].mean(), 2)
            #     max_numeric = round(st.session_state.main_df[numeric_cols[0]].max(), 2)
            # else:
            #     avg_numeric = "N/A"
            #     max_numeric = "N/A"
            # st.subheader("Key Dataset Metrics")
            # st.text(numeric_cols)

            # col1, col2, col3, col4, col5 = st.columns(5)

            # col1.metric(
            #     label="Rows",
            #     value=f"{total_rows:,}"
            # )

            # col2.metric(
            #     label="Columns",
            #     value=total_columns
            # )

            # col3.metric(
            #     label="Missing Values",
            #     value=f"{missing_values:,}"
            # )

            # col4.metric(
            #     label=f"Avg {numeric_cols[0]}" if len(numeric_cols) > 0 else "Average",
            #     value=avg_numeric
            # )

            # col5.metric(
            #     label=f"Max {numeric_cols[0]}" if len(numeric_cols) > 0 else "Maximum",
            #     value=max_numeric
            # )
            # ================rejected=====================================

    # -------------------------------------------------------------------------------------------
            # st.snow()
            st.subheader("Column vs Missing Values:")
            missing = st.session_state.main_df.isnull().sum()
            st.bar_chart(missing[missing > 0], y_label= "Missing Values")
            numeric_cols = st.session_state.main_df.select_dtypes(include="number").columns
            # if numeric_cols:

            # =============bar chart ends============================

            # column = st.selectbox("Choose a column", numeric_cols)
            # st.line_chart(uploaded_df[column])
            #  excluded from no clear sense
            # =======================================================
            corr = st.session_state.main_df.select_dtypes(include="number").corr()
            summary = st.session_state.main_df.describe(include="all").to_string()

            insights = ai_help(
                f"Analyze this dataset summary and provide 5 business insights:\n{summary}"
            )
            st.subheader("Business Insights:")
            st.write(insights)
    with tab2:
        
        question = st.text_input("Ask a question about your data")
        if question:
            prompt3 = f"""
            Columns:
            {list(st.session_state.main_df.columns)}

            Data types:
            {st.session_state.main_df.dtypes.astype(str).to_dict()}

            Dataset Summary:
            {st.session_state.main_df.describe(include='all').to_string()}

            Question:
            {question}
            """

            answer = ai_help(prompt3)

            st.write(answer)

        # st.snow()
    with tab3:
        user_request = st.text_input("Describe your problem")
        if user_request:
            prompt4 = f"""
            You are an expert Python Pandas developer.

            DataFrame name: main_df

            Columns:
            {list(st.session_state.main_df.columns)}

            Data Types:
            {st.session_state.main_df.dtypes.astype(str).to_dict()}

            Sample Data:
            {st.session_state.main_df.head(5).to_dict()}

            Task:
            {user_request}

            Rules:
            1. Return ONLY valid Python Pandas code.
            2. Assume the DataFrame is already loaded as 'st.session_state.main_df'.
            3. Do not create sample data.
            4. Do not explain the code.
            5. Do not use markdown.
            6. Do not wrap the code in ```python.
            7. Store the final result in a variable named 'result'.
            8. If a chart is requested, use Plotly Express and store the figure in a variable named 'fig'.

            Examples:

            Question:
            Top 10 customers by revenue

            Answer:
            result = (
                st.session_state.main_df.groupby("customer_id")["total_amount"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            Question:
            Total revenue by order status

            Answer:
            result = (
                st.session_state.main_df.groupby("order_status")["total_amount"]
                .sum()
                .reset_index()
            )

            Generate the code now.
            """
            code = ai_help(prompt4)
            st.code(code, language="python")
    with tab4:
        st.subheader("Missing Values")


        missing = st.session_state.main_df.isnull().sum()
        st.dataframe(missing[missing > 0])


        st.subheader("Remove duplicates")
        duplicates = st.session_state.main_df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)
        if st.button("Remove Duplicates"):
            st.session_state.main_df = st.session_state.main_df.drop_duplicates()
            st.success("Duplicates removed.")


        st.subheader("Fill missings")
        numeric_cols = st.session_state.main_df.select_dtypes(include="number").columns
        col = st.selectbox("Select Numeric Column", numeric_cols)

        if st.button("Fill Missing with Mean"):
            mean_value = st.session_state.main_df[col].mean()
            st.session_state.main_df[col] = st.session_state.main_df[col].fillna(round(st.session_state.main_df[col].mean(),0), inplace=True)
            st.success(f"Filled missing {col} with average {col}: {round(st.session_state.main_df[col].mean(),0)}")
            missing = st.session_state.main_df.isnull().sum()
            st.dataframe(missing[missing > 0])
        
        # Drop cols
        st.subheader("Drop column")
        cols_to_drop = st.multiselect(
            "Select Columns to Drop",
            st.session_state.main_df.columns
        )

        if st.button("Drop Columns"):
            st.session_state.main_df = st.session_state.main_df.drop(columns=cols_to_drop)
            st.success(f"{cols_to_drop} dropped.")
        st.subheader("Change datatype")
        col = st.selectbox(
        "Select Column",
        st.session_state.main_df.columns
        )

        dtype = st.selectbox(
            "Convert To",
            ["int", "float", "str", "datetime"]
        )

        csv = st.session_state.main_df.to_csv(index=False)

        st.subheader("Download clean data")
        st.download_button(
            "Download Cleaned CSV",
            csv,
            "cleaned_data.csv",
            "text/csv"
        )


else:
    st.error(f"Please upload the csv file.")

st.caption(
    "© 2026 Faizan Ahmed Makki | AI-Powered Data Analytics Platform | All Rights Reserved."
)

