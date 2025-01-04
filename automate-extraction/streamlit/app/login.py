import streamlit as st
import time
from utils.api_request import login_api


st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    success, message = login_api(username, password)
    if success:
        st.session_state.token = message
        st.success("Login successful!")
        st.session_state.logged_in = True
        time.sleep(2)
        st.rerun()
    else:
        st.error(message)