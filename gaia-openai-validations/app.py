from dotenv import load_dotenv
from project_logging.logging_module import log_info, log_success, log_warning, log_error, log_critical
import streamlit as st
from components import db_connection

load_dotenv()

if 'home_page' not in st.session_state:
    st.session_state.home_page = 'home' 
    log_success("NEW PROGRAM EXECUTION\n\n")



st.title("OpenAI Benchmarking with GAIA Dataset")
log_success("Application successfully rendered.")