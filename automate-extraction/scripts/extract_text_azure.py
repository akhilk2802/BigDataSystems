from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
import json
from utils.config import AZURE_CONFIG
from utils.logging_module import log_info, log_error

# Configuration
azure_endpoint = AZURE_CONFIG["endpoint"]
azure_api_key = AZURE_CONFIG["api_key"]

# Directory setup
input_dir = "../downloaded_pdfs"
output_dir = "../extracted_texts/azure/"
os.makedirs(output_dir, exist_ok=True)

def extract_text_azure():
    """
    Extract text from PDFs in a specified directory using Azure Document Intelligence.
    The extracted content is saved as JSON files in an output directory.
    """
    try:
        # Initialize Azure DocumentAnalysisClient
        client = DocumentAnalysisClient(
            endpoint=azure_endpoint,
            credential=AzureKeyCredential(azure_api_key)
        )

        # Ensure input directory exists
        if not os.path.exists(input_dir):
            log_error(f"Input directory does not exist: {input_dir}")
            raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

        for file_name in os.listdir(input_dir):
            if file_name.endswith(".pdf"):
                pdf_file_path = os.path.join(input_dir, file_name)
                try:
                    log_info(f"Processing file: {file_name}")

                    # Analyze the document
                    with open(pdf_file_path, "rb") as file_stream:
                        poller = client.begin_analyze_document("prebuilt-read", file_stream)
                        result = poller.result()

                    # Save extracted text
                    base_file_name = os.path.splitext(file_name)[0]
                    output_file_path = os.path.join(output_dir, f"{base_file_name}.json")
                    
                    # Extract text from lines
                    extracted_text = {
                        "file_name": file_name,
                        "pages": [
                            {
                                "page_number": page.page_number,
                                "text": " ".join([line.content for line in page.lines])
                            }
                            for page in result.pages
                        ]
                    }

                    # Write to JSON
                    with open(output_file_path, "w") as json_file:
                        json.dump(extracted_text, json_file, indent=4)

                    log_info(f"Extracted text saved to {output_file_path}")

                except Exception as e:
                    log_error(f"Failed to process {file_name}: {e}")

    except FileNotFoundError as fnf_error:
        log_error(f"FileNotFoundError: {fnf_error}")
        raise

    except ValueError as val_error:
        log_error(f"ValueError: {val_error}")
        raise

    except Exception as e:
        log_error(f"Unexpected error occurred: {e}")
        raise RuntimeError(f"Unexpected error during Azure text extraction: {e}")