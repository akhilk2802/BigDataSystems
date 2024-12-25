import requests
from utils.logging_module import log_info, log_error
from utils.config import AWS_CONFIG, DATABSE_CONFIG
import boto3
import psycopg2
    
def convert_s3_url_to_presigned(bucket_name, s3_url):
    try:
        session = boto3.Session(profile_name=AWS_CONFIG['profile'])
        s3_client = session.client('s3')
        object_key = s3_url.split(f"https://{bucket_name}.s3.amazonaws.com/")[-1]
        presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=3600)
        return presigned_url
    except Exception as e:
        log_error(f"Error converting S3 URL to pre-signed URL: {e}")
        return None

def fetch_download_pdfs():
    try:
        connection = psycopg2.connect(**DATABSE_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM assignment2.gaia_dataset_tbl WHERE file_extension = 'pdf'")
        records = cursor.fetchall()

        for record in records:
            file_name = record['file_name']
            s3_url = record['s3_url']
            presigned_url = convert_s3_url_to_presigned(AWS_CONFIG['s3_bucket'], s3_url)
            response = requests.get(presigned_url)

            download_dir = "../downloaded_pdfs"
            file_path = f"{download_dir}/{file_name}"


            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                log_info(f"Downloaded: {file_name}")
            else:
                log_error(f"Failed to download: {file_name}, HTTP: {response.status_code}")

        cursor.close()
        connection.close()
    except Exception as e:
        log_error(f"Error in fetch_download_pdfs: {e}")
        raise