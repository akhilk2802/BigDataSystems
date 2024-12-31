import streamlit as st

def is_logged_in():
    return "token" in st.session_state and st.session_state.token is not None