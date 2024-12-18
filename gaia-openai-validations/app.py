from dotenv import load_dotenv
from project_logging.logging_module import log_info, log_success, log_warning, log_error, log_critical
import streamlit as st
from components import db_connection

load_dotenv()

if 'home_page' not in st.session_state:
    st.session_state.home_page = 'home' 
    log_success("NEW PROGRAM EXECUTION\n\n")

# try:
#     db_connection.get_db_connection()
#     logging_module.log_success("Connected to the PostgreSQL database.")
# except:
#     logging_module.log_error("Failed to connect to the PostgreSQL database.")


st.title("OpenAI Benchmarking with GAIA")
log_success("Application successfully rendered.")