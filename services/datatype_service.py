from services.ai_service import ai_help
import pandas as pd
import streamlit as st
import json
import io


def data_summ():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Column Types")
        with st.container(border=True):
            buffer = io.StringIO()
            st.session_state.main_df.info(buf=buffer)
            st.text(buffer.getvalue())
        
        
        # st.text(buffer.getvalue())

    with col2:
        st.subheader("Suggested Column Types")
        with st.container(border=True):

            sample = st.session_state.main_df.head(20).to_csv(index=False)
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
            try:
                ai_df = st.session_state.main_df.copy()
                ai_response = ai_help(prompt1)
                # st.text(ai_response) #debug
                dtype_map = json.loads(ai_response)
            except json.JSONDecodeError:
                st.error(
                    "AI returned an invalid response. Please try again."
                )
            try:
                for col, dtype in dtype_map.items():
                    if dtype == "datetime64[ns]":
                        ai_df[col] = pd.to_datetime(ai_df[col], errors="coerce")

                    elif dtype in ["int64", "float64"]:
                        ai_df[col] = pd.to_numeric(ai_df[col], errors="coerce")

                        if dtype == "int64":
                            ai_df[col] = ai_df[col].astype("Int64")  # nullable integer

                    else:
                        ai_df[col] = ai_df[col].astype(dtype)

            except Exception as e:
                    st.error("An unexpected error occurred. Please try again later.")
            buffer = io.StringIO()
            ai_df.info(buf=buffer)
            st.text(buffer.getvalue())
    if st.button("Continue with AI suggested Column types."):
        st.session_state.updated_cols = True
        st.session_state.main_df = ai_df
        st.success("Column type updated")
        
