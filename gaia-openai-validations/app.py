from dotenv import load_dotenv
from project_logging import logging_module
import streamlit as st
from components import db_connection

load_dotenv()

if 'home_page' not in st.session_state:
    st.session_state.home_page = 'home' 
    logging_module.log_success("NEW PROGRAM EXECUTION\n\n")

try:
    db_connection.get_db_connection()
    logging_module.log_success("Connected to the PostgreSQL database.")
except:
    logging_module.log_error("Failed to connect to the PostgreSQL database.")


st.title("OpenAI Benchmarking with GAIA")

logging_module.log_success("Application successfully rendered.")