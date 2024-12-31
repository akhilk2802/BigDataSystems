import streamlit as st
from app.utils.api_request import register_api

def show():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        success, response = register_api(username, email, password)
        if success:
            st.success("Registration successful! Redirecting to login...")
            st.session_state.page = "login"
            st.experimental_rerun()
        else:
            st.error(response)