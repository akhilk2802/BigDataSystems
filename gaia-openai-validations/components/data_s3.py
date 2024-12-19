import boto3
import os
from dotenv import load_dotenv
import requests
import tempfile
from urllib.parse import urlparse, unquote
from components.etl_logging import log_etl_info, log_etl_success, log_etl_warning, log_etl_error, log_etl_critical


load_dotenv()

RETRIEVAL_EXT = ['.docx', '.txt', '.pdf', '.pptx']
CI_EXT = ['.csv', '.xlsx', '.py', '.zip']
IMG_EXT = ['.jpg', '.png']
ERR_EXT = ['.pdb', '.jsonld']
MP3_EXT = ['.mp3']

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# parse s3 url for bucket name and object key
def parse_s3_url(url):
    """
    Parse an S3 URL into its bucket name and object key.

    Args:
        url (str): The S3 URL to parse.

    Returns:
        tuple: A tuple containing the bucket name and object key.
    """
    parsed_url = urlparse(url)
    bucket_name = parsed_url.netloc.split('.')[0]  # Extract bucket name
    object_key = parsed_url.path.lstrip('/')       # Extract object key
    return bucket_name, object_key

# generate presigned url 
def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """
    Generate a presigned URL for an S3 object.
    """
    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# process data and generate urls
def process_data_generate_url(question, df):
    """
    Fetches data from the database, extracts the S3 URL for the specified question, and generates a pre-signed URL if available.

    Args:
        question (str): The question for which the associated S3 URL needs to be retrieved.

    Returns:
        str: A pre-signed URL for the S3 file if available.
    """
    # Fetch data from the database
    try:
        url = df[df['question'] == question]['s3_url'].values[0]
        log_etl_success(f"Successfully fetched S3 URL for question: {question}")
        bucket_name, object_key = parse_s3_url(url)
        log_etl_info(f"Bucket Name: {bucket_name}, Object Key: {object_key}")
        presigned_url = generate_presigned_url(bucket_name, object_key)
        log_etl_info(f"Presigned URL: {presigned_url}")

        log_etl_success(f"Successfully generated presigned URL for question: {question}")
        return presigned_url
    except IndexError:
        return None


# download file
def download_file(url):
    """
        Downloads a file from the given URL and saves it as a temporary file with the appropriate extension.
    Args:
        url (str): The URL of the file to be downloaded.

    Returns:
        dict: A dictionary containing the following keys:
            - "url" (str): The original URL of the file.
            - "path" (str): The path to the downloaded temporary file.
            - "extension" (str): The file extension of the downloaded file.
    """

    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    filename = os.path.basename(path)
    extension = os.path.splitext(filename)[1]
    
    # Create a temporary file with the correct extension
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=extension)
    
    # Get the file from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the download was successful
    
    # Write the content to the temporary file
    temp.write(response.content)
    temp.close()  # Close the file to finalize writing
    
    return {"url": url, "path": temp.name, "extension": extension}