import streamlit as st

def clear_session():
    st.session_state.token = None
    st.rerun()