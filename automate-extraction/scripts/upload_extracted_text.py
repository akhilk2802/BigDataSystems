import boto3
import os
from utils.logging_module import log_info, log_error
from utils.config import AWS_CONFIG

def upload_extracted_text():
    try:
        session = boto3.Session(profile_name=AWS_CONFIG['profile'])
        s3 = session.client('s3')
        # directory where the extracted text files are saved
        extract_text_dir = "../extracted_texts"
        for file in os.listdir(extract_text_dir):
            if file.endswith('.json'):
                s3.upload_file(file, AWS_CONFIG['s3_bucket'], f"extracted_text/{file}")
                log_info(f"Uploaded {file} to S3")
    except Exception as e:
        log_error(f"Error uploading to S3: {e}")
        raise