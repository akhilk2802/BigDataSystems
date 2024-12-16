import pandas as pd
from datasets import load_dataset
import streamlit as st

@st.cache_data
def load_gaia_dataset():
    dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")
    available_splits = list(dataset.keys())
    st.sidebar.write(f"Available Splits: {available_splits}")
    test_data = pd.DataFrame(dataset['validation'])
    return test_data