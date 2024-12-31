import streamlit as st

def login_form():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    return username, password

def register_form():
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    return username, email, password