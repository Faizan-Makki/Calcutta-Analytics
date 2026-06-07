import streamlit as st
from services.ai_service import ai_help
from components.footer import show_footer

st.header("Generate pandas code")
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

show_footer()
