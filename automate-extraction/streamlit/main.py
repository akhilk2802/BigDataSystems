import streamlit as st
from app.pages import login, register, homepage

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "homepage"

if st.session_state.page == "login":
    login.show()
elif st.session_state.page == "register":
    register.show()
elif st.session_state.page == "homepage":
    homepage.show()

# Sidebar Navigation
if st.sidebar.button("Login"):
    st.session_state.page = "login"
    st.experimental_rerun()

if st.sidebar.button("Register"):
    st.session_state.page = "register"
    st.experimental_rerun()

if st.sidebar.button("Homepage"):
    st.session_state.page = "homepage"
    st.experimental_rerun()