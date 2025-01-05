import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False



def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page("login.py", title="Login", icon=":material/login:")
register_page = st.Page("register.py", title="Register", icon=":material/assignment_ind:")
logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
homepage_page = st.Page("homepage.py", title="Homepage", icon=":material/home:")
extractor_page = st.Page("extractor.py", title="PDF Extractor", icon=":material/insert_drive_file:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Home": [homepage_page],
            "Account": [logout_page],
            "PDF Extractor": [extractor_page]
            
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