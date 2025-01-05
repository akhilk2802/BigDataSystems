import requests
import pandas as pd
import streamlit as st
import json

def fetch_data_from_api(data: dict):
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = requests.get("http://127.0.0.1:8000/fetch-all", headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None
    
def get_annotator_metadata(question):
    df = st.session_state.data_frame
    if question in df['Question'].values:
        row = df.loc[df['Question'] == question]
        annotator_metadata_json = row['Annotator Metadata'].values[0]
        try:
            annotator_metadata = json.loads(annotator_metadata_json)
            return annotator_metadata
        except json.JSONDecodeError:
            st.error("Error decoding annotator metadata.")
            return None
    else:
        return None