import streamlit as st
import json
from components.evaluation import evaluate_model
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

# st.write("Available Columns:", test_data.columns)

# Test Case Selection
test_case = st.sidebar.selectbox(
    "Select a Test Question:", test_data['Question']
)

# Display Test Case Context
# st.subheader("Test Case Context")
# context = test_data.loc[test_data['Question'] == test_case, 'context'].values[0]
# st.write(context)

selected_row = test_data.loc[test_data['Question'] == test_case]

selected_row_dict = selected_row.to_dict(orient="records")[0]
selected_row_json = json.dumps(selected_row_dict, indent=4)
# print("Selected Row in JSON Format:\n", selected_row_json)



if not selected_row.empty:
    st.subheader("Test Case Details")
    st.write(selected_row)
else:
    st.error("Selected Question not found in the dataset.")


# Display Test Case Context
annotator_metadata = selected_row['Annotator Metadata'].values[0]
# print("Annotator Metadata:", annotator_metadata)


# Model Evaluation
if st.button("Evaluate with OpenAI"):
    model_response, correct_answer = evaluate_model(test_data, test_case, annotator_metadata)
    # display_evaluation_metrics(test_case, correct_answer, model_response)
    # display_feedback_form(test_case, correct_answer, model_response)

# Show Evaluation Report
# if st.checkbox("Show Evaluation Summary Report"):
    # show_evaluation_report()