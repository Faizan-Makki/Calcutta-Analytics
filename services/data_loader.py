import streamlit as st
import pandas as pd

def load_dataframe(uploaded_file):
    # uploaded_df = 
    return pd.read_csv(uploaded_file)
    # st.write(uploaded_df)


# st.success(f"Uploaded: {uploaded.name} ({uploaded.size} bytes)")
#         uploaded_df = pd.read_csv(uploaded)

#         tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Ask AI","Generate pandas code","Clean Data"])
#         with tab1:
#             st.write(uploaded_df)