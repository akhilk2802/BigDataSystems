from huggingface_hub import login
from dotenv import load_dotenv
import os
from utils.logging_module import log_info, log_success, log_warning, log_error, log_critical
from utils.config import HF_CONFIG as hf_config

def login_hf():
    try:
        login(token=hf_config['token'])
        log_success('Hugging Face login successful')
        print("Logged in to Hugging Face successfully.")
    except Exception as e:
        print(f"Failed to login to Hugging Face: {e}")
        log_error(f'Failed to login to Hugging Face: {e}')
        raise