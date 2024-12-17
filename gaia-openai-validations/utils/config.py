from dotenv import load_dotenv
import os
import openai
from huggingface_hub import login

# Initialize API Keys from .env file
def initialize_api_keys():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    hf_token = os.getenv("HF_TOKEN")

    if not openai.api_key or not hf_token:
        raise ValueError("Missing API Keys in environment variables.")
    
    login(hf_token)