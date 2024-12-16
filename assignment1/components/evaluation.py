import openai
import streamlit as st
from transformers import pipeline


# Evaluate Model Response
def evaluate_model(test_data, test_case, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context} Question: {test_case}"}
            ],
            max_tokens=200
        )
        model_response = response['choices'][0]['message']['content'].strip()
        correct_answer = test_data.loc[test_data['Question'] == test_case, 'Answer'].values[0]
        return model_response, correct_answer
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API Error: {e}, Status Code: {getattr(e, 'http_status', 'N/A')}")
        return None, None
    

qa_pipeline = pipeline("question-answering", model="deepset/bert-base-cased-squad2")

def evaluate_model_bert(test_data, test_case, context):
    try:

        if isinstance(context, dict):
            context = " ".join(f"{key}: {value}" for key, value in context.items())

        # print("Context:", context)
        # print("Test Case:", test_case)

        if not test_case or not context:
            raise ValueError("Invalid Inputs: Both question and context are required.")
        result = qa_pipeline(
            question=test_case,
            context=context
        )

        model_response = result['answer'].strip()

        matching_row = test_data.loc[test_data['Question'] == test_case, "Final answer"]        

        if not matching_row.empty:
            correct_answer = matching_row.values[0]
        else:
            correct_answer = "Answer Not Found"

        return model_response, correct_answer
    except Exception as e:
        st.error(f"Hugging Face Model Error: {e}")
        return None, None