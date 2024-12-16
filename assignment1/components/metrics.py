import streamlit as st
import pandas as pd
from evaluate import load

# Load BLEU Metric
bleu = load("bleu")
FEEDBACK_FILE = "evaluation_results.csv"

# Display Evaluation Metrics
def display_evaluation_metrics(test_case, correct_answer, model_response):
    exact_match = model_response == correct_answer
    bleu_score = bleu.compute(
        predictions=[model_response],
        references=[[correct_answer]]
    )['bleu']

    st.metric("Exact Match", "✅" if exact_match else "❌")
    st.metric("BLEU Score", f"{bleu_score:.2f}")

# Show Evaluation Summary Report
def show_evaluation_report():
    if os.path.exists(FEEDBACK_FILE):
        summary_df = pd.read_csv(FEEDBACK_FILE)
        st.subheader("Evaluation Report")
        st.dataframe(summary_df)
    else:
        st.warning("No evaluation results found. Please run evaluations first.")