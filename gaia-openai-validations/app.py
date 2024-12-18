import streamlit as st
import json
from components.evaluation import evaluate_model, evaluate_model_bert
from components.feedback import display_feedback_form, save_evaluation_results
from components.metrics import display_evaluation_metrics, show_evaluation_report
from components.dataset import load_gaia_dataset
from utils.config import initialize_api_keys

# Initialize API Keys
initialize_api_keys()

# Streamlit UI
st.title("Model Evaluation Tool")
st.sidebar.header("Select Evaluation Test Case")

# Load Dataset
test_data = load_gaia_dataset()


# Test Case Selection
test_case = st.sidebar.selectbox(
    "Select a Test Question:", test_data['Question']
)

selected_row = test_data.loc[test_data['Question'] == test_case]

selected_row_dict = selected_row.to_dict(orient="records")[0]
selected_row_json = json.dumps(selected_row_dict, indent=4)



if not selected_row.empty:
    st.write("Selected test Question: ", selected_row['Question'].values[0])
else:
    st.error("Selected Question not found in the dataset.")


annotator_metadata = selected_row['Annotator Metadata'].values[0]


if st.button("Evaluate with BERT"):
    model_response, correct_answer = evaluate_model_bert(test_data, test_case, annotator_metadata)
    if model_response and correct_answer:
        st.write("Model Response: ", model_response)
        st.write("Correct Answer:", correct_answer)

        display_evaluation_metrics(test_case, correct_answer, model_response)
        display_feedback_form(test_case, correct_answer, model_response)

if st.button("Evaluate with OpenAI"):
    model_response, correct_answer = evaluate_model(test_data, test_case, annotator_metadata)
    # display_evaluation_metrics(test_case, correct_answer, model_response)
    # display_feedback_form(test_case, correct_answer, model_response)

if st.checkbox("Show Evaluation Summary Report"):
    show_evaluation_report()