import streamlit as st
from utils.api_request import register_api


st.title("Register")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):
    success, response = register_api(username, email, password)
    if success:
        print("Registration successful!")
        st.success("Registration successful!", icon="✅")
        st.session_state.registration_success = True
        # st.rerun()
    else:
        st.error(f"Registration failed: {response}", icon="❌")