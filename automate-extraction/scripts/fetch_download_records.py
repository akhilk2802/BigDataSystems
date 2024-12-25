import psycopg2
from psycopg2.extras import DictCursor
import requests
from utils.config import DATABSE_CONFIG as db_config
from utils.config import HF_CONFIG as hf_config
from utils.config import AWS_CONFIG as aws_config
from utils.logging_module import log_info, log_success, log_warning, log_error, log_critical
import boto3


def fetch_download_records():
    try:
        # Connect to DB
        connection = psycopg2.connect(**db_config)
        log_info("Connected to the database")
        # Create a cursor object
        cursor = connection.cursor(cursor_factory=DictCursor)
        select_query = "SELECT * FROM assignment2.gaia_dataset_tbl WHERE trim(file_name) != ''"
        cursor.execute(select_query)
        records = cursor.fetchall()
        log_success("Records fetched successfully")

        headers = {"Authorization": f"Bearer {hf_config['token']}"}
        hugging_face_base_url = hf_config['base_url']
        session = boto3.Session(profile_name=aws_config['profile'])
        

        for record in records:
            file_name = record['file_name'].strip()
            split_type = record['split_type']
            if split_type in ['test', 'validation']:
                file_url = f"{hugging_face_base_url}/{split_type}/{file_name}"  # Dynamic URL construction
                try:
                    response = requests.get(file_url, headers=headers)
                    if response.status_code == 200:
                        file_data = response.content
                        log_success(f"Downloaded {file_name} from Hugging Face")

                        s3_key = f"gaia_files/{file_name}"
                        s3 = session.client('s3')
                        s3.put_object(Bucket=aws_config['s3_bucket'], Key=s3_key, Body=file_data)
                        s3_url = f"https://{aws_config['s3_bucket']}.s3.amazonaws.com/{s3_key}"
                        log_success(f"Uploaded {file_name} to S3")

                        update_s3url_query = """
                        UPDATE assignment2.gaia_dataset_tbl
                        SET s3_url = %s
                        WHERE task_id = %s
                        """
                        cursor.execute(update_s3url_query, (s3_url, record['task_id']))
                        connection.commit()
                        log_success(f"Updated record {record['task_id']} with S3 URL")

                        update_file_ext_query = """
                        UPDATE assignment2.gaia_dataset_tbl
                        SET file_extension = RIGHT(file_name, LENGTH(file_name) - POSITION('.' IN file_name))
                        WHERE task_id = %s
                        """
                        cursor.execute(update_file_ext_query, (record['task_id'],))
                        connection.commit()
                        log_success(f"Updated record {record['task_id']} with file extension")
                    else:
                        log_warning(f"Failed to download file {file_name} from {split_type} split. Status code: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    log_error(f"Error downloading file {file_name} from {split_type} split: {e}")
            else:
                log_warning(f"Unknown split type '{split_type}' for file {file_name}")
    except Exception as e:
        log_critical("Failed to fetch records")
        log_error(f"Error: {e}")
        raise
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            log_success("Database connection closed successfully")
            if 'cursor' in locals() and cursor:
                log_success("Cursor closed successfully")
            else:
                log_warning("Cursor not found to close")
