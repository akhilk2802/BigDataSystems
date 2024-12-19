import streamlit as st
import json 
from components.data_read import fetch_data_from_db, fetch_data_from_db_dashboards

if 'data_frame' not in st.session_state:
    st.session_state.data_frame = fetch_data_from_db()
# if 'openai_client' not in st.session_state:
#     st.session_state.openai_client = 


with st.sidebar:
    difficulty_levels = ["All"] + st.session_state.data_frame["level"].unique().tolist()
    level_filter = st.selectbox("Dificulty level", difficulty_levels, index=None)
    file_ext = ['PDF', 'DOCX', 'TXT', 'PPTX', 'CSV', 'XLSX', 'PY', 'ZIP', 'JPG', 'PNG', 'PDB', 'JSONLD', 'MP3']
    extension_filter = st.selectbox("File extension", file_ext, index=None)

if level_filter == "All":
    filtered_questions = st.session_state.data_frame
else:
    filtered_questions = st.session_state.data_frame[str(st.session_state.data_frame['level'] == level_filter)]

# Display Questions in Selectbox
if not filtered_questions.empty:
    selected_question = st.selectbox(
        "Select a Question", 
        filtered_questions["question"].tolist()
    )
    st.success(f"You selected: {selected_question}")
else:
    st.warning("No questions found for the selected difficulty level.")