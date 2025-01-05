import streamlit as st
import time
from utils.api_request import login_api
from utils.fetch_data import fetch_data_from_api


st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    success, message = login_api(username, password)
    if success:
        st.session_state.token = message
        st.session_state.username = message["username"]
        st.success("Login successful!")
        st.session_state.logged_in = True

        df = fetch_data_from_api(message)
        if df is not None:
            st.session_state.data_frame = df
            st.success("Data fetched and stored successfully!")

        time.sleep(2)
        st.rerun()
    else:
        st.error(message)