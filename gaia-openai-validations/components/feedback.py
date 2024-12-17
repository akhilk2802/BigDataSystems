import streamlit as st
import pandas as pd
import os

FEEDBACK_FILE = "evaluation_results.csv"

# Feedback Management Form
def display_feedback_form(test_case, correct_answer, model_response):
    user_feedback = st.text_input("Suggest Correct Answer (Optional):")
    if user_feedback:
        st.success("Feedback Saved!")
    save_evaluation_results(test_case, correct_answer, model_response, user_feedback)

# Save Evaluation Results
def save_evaluation_results(test_case, correct_answer, model_response, user_feedback):
    feedback_data = {
        "Test Case": test_case,
        "Expected Answer": correct_answer,
        "Model Response": model_response,
        "User Feedback": user_feedback or "N/A"
    }

    feedback_df = pd.DataFrame([feedback_data])

    # Check if file exists before reading
    if os.path.exists(FEEDBACK_FILE):
        try:
            existing_data = pd.read_csv(FEEDBACK_FILE)
            feedback_df = pd.concat([existing_data, feedback_df], ignore_index=True)
        except pd.errors.EmptyDataError:
            st.warning("Feedback file is empty, creating a new file.")
    
    # Save to CSV
    feedback_df.to_csv(FEEDBACK_FILE, index=False)
    st.success("Evaluation Results Saved!")