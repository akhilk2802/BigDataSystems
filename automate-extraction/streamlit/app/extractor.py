import streamlit as st
import pandas as pd
import requests
import os
import tempfile
from utils.s3 import parse_s3_url
from utils.api_request import fetch_context, response_openai
from utils.fetch_data import get_annotator_metadata

st.title("Validation Tool with extracted texts from PDFs")

if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = {}

if 'data_frame' not in st.session_state:
    st.session_state.data_frame = pd.DataFrame()

if "username" in st.session_state:
    st.subheader(f"Welcome {st.session_state.username}!")
else:
    st.subheader("Welcome!")

st.sidebar.header("Filter Options")

difficulty_levels = ["All"] + sorted(st.session_state["data_frame"]['Level'].unique().tolist())
selected_level = st.sidebar.selectbox("Select Difficulty Level", difficulty_levels)

split_types = ["All"] + sorted(st.session_state["data_frame"]['split_type'].unique().tolist())
selected_split_type = st.sidebar.selectbox("Select Split Type", split_types)

file_types = ["All"] + sorted(
    [ext for ext in st.session_state["data_frame"]['file_extension'].unique() if ext is not None]
)
selected_file_type = st.sidebar.selectbox("Select File Type", file_types)

filtered_data = st.session_state["data_frame"].copy()
if selected_level != "All":
    filtered_data = filtered_data[filtered_data['Level'] == selected_level]

if selected_split_type != "All":
    filtered_data = filtered_data[filtered_data['split_type'] == selected_split_type]

if selected_file_type != "All":
    filtered_data = filtered_data[filtered_data['file_extension'] == selected_file_type]

# st.subheader("Select a Question")
if filtered_data.empty:
    st.warning("No records found. Please adjust your filters.")
else:
    selected_question = st.selectbox(
        "Choose a Question",
        ["Select a question..."] + filtered_data['Question'].dropna().unique().tolist(),
        index=0
    )

if selected_question != "Select a question...":
    st.session_state.question = selected_question
    print("Selected Question: ", st.session_state.question)
    st.session_state.questionId = filtered_data.loc[filtered_data['Question'] == selected_question, 'task_id'].values[0]
    print("QuestionId: ",st.session_state.questionId)
    st.write("Selected Question (You may edit the question)")
    st.text_area("Question:", selected_question, height=120)
   
    final_answer = filtered_data.loc[filtered_data['Question'] == selected_question, 'Final answer'].values[0]
    st.text_area("Answer:", final_answer, height=80, disabled=True)

    s3_url = filtered_data.loc[filtered_data['Question'] == selected_question, 's3_url'].values[0]

    if pd.isna(s3_url):
        st.info("No file available.")
    else:
        try:
            bucket_name, object_key = parse_s3_url(s3_url)
            # presigned_url = generate_presigned_url(bucket_name, object_key)
            presigned_url = "https://gaia-extraction.s3.amazonaws.com/assignment2/gaia_dataset_tbl/1.json"

            if presigned_url:
                response = requests.get(presigned_url)

                if response.status_code == 200:
                    file_ext = os.path.splitext(object_key)[1]

                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                        temp_file.write(response.content)
                        temp_file_path = temp_file.name

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
        if st.button("Extract Text from pdf with Azure"):
            success, response = fetch_context(st.session_state.questionId, "azure", st.session_state.token["access_token"])
            if success:
                print("Response: ", response)
                pages_data = response.get('context', {}).get('pages', [])
                concatenated_text = " ".join(page["text"] for page in pages_data)
                st.session_state.extracted_text = concatenated_text
    with col2:
        if st.button("Extract Text from pdf with PyPDF"):
            success, response = fetch_context(st.session_state.questionId, "pypdf", st.session_state.token["access_token"])
            if success:
                print("Response: ", response)
                text_content = response.get('context', {}).get('text', '')
                st.session_state.extracted_text = text_content

    openai_models = [
    "GPT-4o",
    "GPT-4o mini",
    "o1",
    "o1 mini",
    "GPT-3.5 Turbo",
    "GPT-4",

    ]

    selected_model = st.selectbox("Select an OpenAI model:", openai_models)
    
    if st.button("Ask GPT"):
        success, response = response_openai(st.session_state.question, st.session_state.extracted_text, selected_model, st.session_state.token["access_token"])
        if success:
            st.write(response["response"])
            if response["response"] == final_answer:
                st.success("Correct answer!")
            else:
                st.error("Incorrect answer.")
        else:
            st.error(response)

    show_steps = st.checkbox("Show annotator steps")
    if show_steps:
        annotator_metadata = get_annotator_metadata(selected_question)
        if annotator_metadata and 'Steps' in annotator_metadata:
            steps = annotator_metadata['Steps']
            st.text_area("Annotator Steps:", steps, height=300)
            if st.button("Ask GPT Again"):
                success, response = response_openai(st.session_state.question, steps, selected_model, st.session_state.token["access_token"])
                if success:
                    st.write(response["response"])
                    if response["response"] == final_answer:
                        st.success("Correct answer!")
                    else:
                        st.error("Incorrect answer.")
                else:
                    st.error(response)
        else:
            st.warning("No annotator steps found for this question.")

