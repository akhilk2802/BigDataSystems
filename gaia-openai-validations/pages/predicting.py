import streamlit as st
import json 
import os
import pandas as pd
from components.data_read import fetch_data_from_db, fetch_data_from_db_dashboards
from project_logging.logging_module import log_info, log_error, log_success
from components.data_s3 import generate_presigned_url, parse_s3_url, download_file
import requests
from openai.opeanai_client import OpenAIClient
from openai.openai_methods import ask_gpt, answer_validation_check

import tempfile
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Predicting", layout="wide")

if "data_frame" not in st.session_state:
    try:
        st.session_state["data_frame"] = fetch_data_from_db()
        log_info("Data loaded successfully into session state.")
    except Exception as e:
        log_error(f"Error loading data from the database: {e}")
        st.error("Error loading data from the database.")
        st.stop()

if "openai_client" not in st.session_state:
    try:
        st.session_state["openai_client"] = OpenAIClient(api_key=openai_api_key)
        log_info("OpenAI Client initialized successfully.")
    except Exception as e:
        log_error(f"Error initializing OpenAI Client: {e}")
        st.error("Error initializing OpenAI Client.")
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
        ["Select a question..."] + filtered_data['Question'].dropna().unique().tolist(), 
        index=0
    )

gpt_models = {
    "GPT-4o": "Optimized for large contexts",
    "GPT-4": "Accurate but slower",
    "GPT-3.5-turbo": "Faster but less accurate",
}

    # Check if a question is selected
if selected_question != "Select a question...":
    # Display the Question Text (Editable)
    st.subheader("Selected Question (You may edit the question)")
    st.text_area("Question:", selected_question, height=150)

    # Show the Final Answer (Read-Only)
    final_answer = filtered_data.loc[filtered_data['Question'] == selected_question, 'Final answer'].values[0]
    st.subheader("Final Answer")
    st.text_area("Answer:", final_answer, height=150, disabled=True)

    st.subheader("Download File")
    s3_url = filtered_data.loc[filtered_data['Question'] == selected_question, 's3_url'].values[0]

    if pd.isna(s3_url):
        st.info("No file available.")
    else:
        try:
            # Generate Presigned URL
            bucket_name, object_key = parse_s3_url(s3_url)
            presigned_url = generate_presigned_url(bucket_name, object_key)

            if presigned_url:
                # Download the file temporarily
                response = requests.get(presigned_url)
                
                if response.status_code == 200:
                    file_ext = os.path.splitext(object_key)[1]

                    # Create a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name

                    # Provide the file for download
                    with open(temp_file_path, "rb") as file:
                        st.download_button(
                            label="Download File",
                            data=file,
                            file_name=f"download{file_ext}",
                        )
                else:
                    st.error("Error in downloading the file.")
            else:
                st.error("Error generating the download link.")
        except Exception as e:
            st.error(f"Error when downloading: {e}")

    col1, col2 = st.columns(2)
    with col1:
        selected_model = st.selectbox(
            "Select GPT Model",
            options=["Select a model..."] + [f"{model} - {desc}" for model, desc in gpt_models.items()],
            index=0,
            key="gpt_model_selection"
        )

    if selected_model != "Select a model...":
        model_name = selected_model.split(" - ")[0]
    else:
        model_name = None


    # Display error if no model is selected
    if model_name is None:
        st.error("Please select a GPT model before proceeding.")

    # Ask GPT Button
    if st.button("Ask GPT"):
        if model_name:
            st.success(f"You have selected {model_name} for the query.")

            file_details = None
            if not pd.isna(s3_url):
                file_details = download_file(s3_url)
                if "error" in file_details:
                    st.error(file_details["error"])
                    st.stop()
            if file_details and file_details['extension'] == ".mp3":  
                system_content = st.session_state.openai_client.audio_system_content
                format_type = 1
            else:
                system_content = st.session_state.openai_client.val_system_content
                format_type = 0
            ai_response = ask_gpt(st.session_state.openai_client, system_content, selected_question, format_type, selected_model, file_details)
            if "Error" in ai_response:
                st.error(ai_response)
            else:
                st.subheader("GPT Response")
                st.text_area("Response:", ai_response, height=200)
                if answer_validation_check(final_answer, ai_response):
                    st.success("The response is correct!")
                else:
                    st.error("The response is incorrect.")
        else:
            st.error("Please select a GPT model before proceeding.")

