import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page("login.py", title="Login")
register_page = st.Page("register.py", title="Register")
logout_page = st.Page(logout, title="Logout")
homepage_page = st.Page("homepage.py", title="Homepage")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Home": [homepage_page],
            "Account": [logout_page]
        }
    )
else:
    pg = st.navigation(
        {
            "Home": [homepage_page],
            "Account": [login_page, register_page]
        }
    )


pg.run()