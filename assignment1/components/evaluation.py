import openai
import streamlit as st

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