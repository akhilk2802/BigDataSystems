import pandas as pd
import json
from datasets import load_dataset
from utils.logging_module import log_info, log_success, log_warning, log_error, log_critical
from utils.config import DATABSE_CONFIG as db_config


def process_dataset():
    try:
        dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")
        log_success("Dataset loaded successfully.")
        print("Dataset loaded successfully.")

        # Convert splits to pandas dataframes
        validation_df = dataset['validation'].to_pandas()
        test_df = dataset['test'].to_pandas()
        log_info("Dataset splits converted to pandas dataframes.")

        # Add split type column to dataframes
        validation_df['split_type'] = 'validation'
        test_df['split_type'] = 'test'
        log_info("Added split type column to dataframes.")

        # Combine dataframes
        combined_df = pd.concat([validation_df, test_df], ignore_index=True)

        # convert Annotator Metadata column to json string
        combined_df['Annotator Metadata'] = combined_df['Annotator Metadata'].apply(json.dumps)
        log_info("Annotator Metadata column converted to json string.")

        # store the dataframe to directory
        dataframe_path = "utils/data/gaia_dataset.csv"
        combined_df.to_csv(dataframe_path, index=False)
        log_success(f"Dataset saved to {dataframe_path}.")
    except Exception as e:
        log_error("Failed to load dataset.")
        print(f"Error fetching dataset: {e}")
        raise

