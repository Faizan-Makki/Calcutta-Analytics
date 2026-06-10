import streamlit as st
import json
from services.ai_service import ai_help


def get_kpi(df):
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
        # st.warning("hulul")
            # data = ai_help(prompt2)