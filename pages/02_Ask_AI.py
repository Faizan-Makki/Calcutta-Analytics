import streamlit as st
from services.ai_service import ai_help
from components.upload import show_upload
from services.data_loader import load_dataframe
from components.footer import show_footer

st.header("Ask a question about your data")

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

question = st.text_input("Ask a question.")
if question:
    
    prompt3 = f"""
    Columns:
    {list(df.columns)}

    Data types:
    {df.dtypes.astype(str).to_dict()}

    Dataset Summary:
    {df.describe(include='all').to_string()}

    Question:
    {question}
    """

    answer = ai_help(prompt3)

    st.write(answer)

show_footer()