import streamlit as st
def show_header():
    header_col1, header_col2 = st.columns([1,5])

    with header_col1:
        st.image("media/logo2.png", width=120)

    with header_col2:
        st.markdown('<h1 class="corporate-title">CALCUTTA ANALYTICS</h1>', unsafe_allow_html=True)
        st.markdown('<p class="corporate-tagline">AI-Powered Analytics for Modern Decision Making</p>', unsafe_allow_html=True)