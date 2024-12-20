import streamlit as st
import json 
import os
import pandas as pd
from components.data_read import fetch_data_from_db, fetch_data_from_db_dashboards
from project_logging.logging_module import log_info, log_error, log_success
from components.data_s3 import generate_presigned_url, parse_s3_url
import requests
import tempfile

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
        ["Select a question..."] + filtered_data['Question'].dropna().unique().tolist(), 
        index=0
    )

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

    st.subheader("Prompt with GPT")
    if st.button("Ask GPT"):
        try:
            # Call GPT function here (mock or real implementation)
            st.info("Processing your request...")

            # Example function call - Replace this with actual GPT query logic
            gpt_response = "This is a mock response from GPT-4."
            st.success("GPT Response received successfully!")
            
            # Display the GPT response
            st.text_area("GPT Response:", gpt_response, height=150, disabled=True)

        except Exception as e:
            st.error(f"Error querying GPT: {e}")

