import streamlit as st
from app.utils.api_request import login_api

def show():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, message = login_api(username, password)
        if success:
            st.session_state.token = message  # Store token in session
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error(message)