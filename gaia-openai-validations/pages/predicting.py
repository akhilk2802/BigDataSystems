import streamlit as st
import json 
import pandas as pd
from components.data_read import fetch_data_from_db, fetch_data_from_db_dashboards
from project_logging.logging_module import log_info, log_error, log_success

st.set_page_config(page_title="Predicting", layout="wide")

if "data_frame" not in st.session_state:
    try:
        st.session_state["data_frame"] = fetch_data_from_db()
        log_info("Data loaded successfully into session state.")
    except Exception as e:
        log_error(f"Error loading data from the database: {e}")
        st.error("Error loading data from the database.")
        st.stop()


st.sidebar.header("Filter Options")

difficulty_levels = ["All"] + sorted(st.session_state["data_frame"]['Level'].unique().tolist())
selected_level = st.sidebar.selectbox("Select Difficulty Level", difficulty_levels)


document_types = ["All"] + sorted(
    [ext for ext in st.session_state["data_frame"]['file_extension'].unique() if ext is not None]
)
selected_doc_type = st.sidebar.selectbox("Select Document Type", document_types)

filtered_data = st.session_state["data_frame"].copy()

if selected_level != "All":
    filtered_data = filtered_data[filtered_data['Level'] == selected_level]

if selected_doc_type != "All":
    filtered_data = filtered_data[filtered_data['file_extension'] == selected_doc_type]

st.header("Select a Question")
if filtered_data.empty:
    st.warning("No records found. Please adjust your filters.")
else:
    selected_question = st.selectbox(
        "Choose a Question", 
        filtered_data['Question'].dropna().unique().tolist()
    )
