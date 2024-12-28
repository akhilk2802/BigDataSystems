import boto3
import os
from utils.logging_module import log_info, log_error
from utils.config import AWS_CONFIG

def upload_extracted_text():
    try:
        session = boto3.Session(profile_name=AWS_CONFIG['profile'])
        s3 = session.client('s3')
        
        # Directories for extracted text files
        directories = {
            "pypdf": "../extracted_texts/pypdf",
            "azure": "../extracted_texts/azure"
        }
        for tool, directory in directories.items():
            for file in os.listdir(directory):
                if file.endswith('.json'):
                    file_path = os.path.join(directory, file)
                    s3_key = f"extracted_text/{tool}/{file}"
                    s3.upload_file(file_path, AWS_CONFIG['s3_bucket'], s3_key)
                    log_info(f"Uploaded {file} from {tool} to S3 at {s3_key}")
    except Exception as e:
        log_error(f"Error uploading to S3: {e}")