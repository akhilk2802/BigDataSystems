import os
from datasets import load_dataset
from huggingface_hub import login
import json
from db_connection import get_db_connection
from dotenv import load_dotenv
from project_logging.etl_logging import log_etl_info, log_etl_success, log_etl_warning, log_etl_error, log_etl_critical
from sqlalchemy import create_engine, text
import boto3
import requests



load_dotenv()

# getting env variables
huggingface_token = os.getenv('HF_TOKEN')
aws_rds_host = os.getenv('AWS_RDS_HOST')
aws_rds_user = os.getenv('AWS_RDS_USERNAME')
aws_rds_password = os.getenv('AWS_RDS_PASSWORD')
aws_rds_port = os.getenv('AWS_RDS_DB_PORT', '5432')
aws_rds_database = os.getenv('AWS_RDS_DATABASE')
aws_s3_bucket = os.getenv('AWS_S3_BUCKET')
aws_s3_region = os.getenv('AWS_S3_REGION')
aws_s3_access_key = os.getenv('AWS_S3_ACCESS_KEY')
aws_s3_secret_key = os.getenv('AWS_S3_SECRET_KEY')
aws_s3_endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL')

# login to huggingface
login(token=huggingface_token)

# connect to db
try:
    connection_string = f"postgresql+psycopg2://{aws_rds_user}:{aws_rds_password}@{aws_rds_host}:{aws_rds_port}/{aws_rds_database}"
    engine = create_engine(connection_string)
    log_etl_success("PostgreSQL connection engine created successfully.")
except Exception as e:
    log_etl_error(f"Failed to create PostgreSQL connection engine. Error: {e}")
    raise

#login with huggingface token
try:
    login(token=huggingface_token)
    log_etl_success("Huggingface login successful.")
except Exception as e:
    log_etl_error(f"Failed to login to Huggingface. Error: {e}")
    raise

# load dataset
try:
    dataset = load_dataset("gaia-benchmark/GAIA", "2023_all")
    log_etl_success("Dataset loaded successfully.")
except Exception as e:
    log_etl_error(f"Failed to load dataset. Error: {e}")
    raise

# convert validation split to pandas dataframe
try:
    # convert validation split to pandas dataframe
    validation_df = dataset['validation'].to_pandas()
    log_etl_success("Validation split converted to pandas dataframe successfully.")

    # convert Annotator Metadata column to json string
    validation_df['Annotator Metadata'] = validation_df['Annotator Metadata'].apply(json.dumps)
    log_etl_success("Annotator Metadata column converted to json string successfully.")

    # convert the dataframe to sql table
    validation_df.to_sql(
        schema='assignment1',
        name='gaia_metadata_tbl',
        con=engine,
        if_exists='replace',
        index=False
    )
    log_etl_success("Validation split converted to SQL table successfully.")
except Exception as e:
    log_etl_error(f"Failed to convert validation split to pandas dataframe. Error: {e}")
    raise

alter_table_query = """
ALTER TABLE assignment1.gaia_metadata_tbl
ADD COLUMN IF NOT EXISTS s3_url VARCHAR(255),
ADD COLUMN IF NOT EXISTS file_extension VARCHAR(255);
"""

# Execute the ALTER TABLE Query
try:
    with engine.connect() as connection:
        connection.execute(text(alter_table_query))
        log_etl_success("Columns 's3_url' and 'file_extension' added successfully.")
except Exception as e:
    log_etl_error(f"Error altering table to add columns: {e}")
    raise

try:
    # Initialize S3 Client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_s3_access_key,
        aws_secret_access_key=aws_s3_secret_key,
        region_name=aws_s3_region,
        endpoint_url=aws_s3_endpoint_url  # Optional, if using custom S3 service
    )
    log_etl_success("Connected to AWS S3 bucket successfully.")
except Exception as e:
    log_etl_error(f"Error connecting to AWS S3: {e}")
    raise

huggingface_base_url = "https://huggingface.co/datasets/gaia-benchmark/GAIA/resolve/main/2023/validation/"

# Fetch Records and Process Files
try:
    connection = get_db_connection()
    headers = {"Authorization": f"Bearer {huggingface_token}"}

    if connection:
        cursor = connection.cursor(dictionary=True)

        # Fetch records with non-null file_name
        select_query = "SELECT * FROM assignment1.gaia_metadata_tbl WHERE trim(file_name) != ''"
        cursor.execute(select_query)
        records = cursor.fetchall()
        log_etl_success(f"Fetched records from assignment1.gaia_metadata_tbl.")

        for record in records:
            task_id = record['task_id']
            file_name = record['file_name'].strip()

            # Download file from Hugging Face
            file_url = huggingface_base_url + file_name
            try:
                response = requests.get(file_url, headers=headers)
                if response.status_code == 200:
                    file_data = response.content
                    log_etl_success(f"Downloaded {file_name} from Hugging Face.")

                    # Upload the file to S3
                    s3_key = f"gaia_files/{file_name}"
                    s3.put_object(Bucket=aws_s3_bucket, Key=s3_key, Body=file_data)
                    s3_url = f"https://{aws_s3_bucket}.s3.amazonaws.com/{s3_key}"
                    log_etl_success(f"Uploaded {file_name} to S3 at {s3_url}")

                    # Update S3 URL in PostgreSQL
                    update_s3url_query = """
                    UPDATE assignment1.gaia_metadata_tbl
                    SET s3_url = %s
                    WHERE task_id = %s
                    """
                    cursor.execute(update_s3url_query, (s3_url, task_id))
                    connection.commit()
                    log_etl_success(f"Updated record {task_id} with S3 URL.")

                    # Update file extension in PostgreSQL
                    update_file_ext_query = """
                    UPDATE assignment1.gaia_metadata_tbl
                    SET file_extension = RIGHT(file_name, LENGTH(file_name) - POSITION('.' IN file_name))
                    WHERE task_id = %s
                    """
                    cursor.execute(update_file_ext_query, (task_id,))
                    connection.commit()
                    log_etl_success(f"Updated record {task_id} with file extension.")

                else:
                    log_etl_error(f"Failed to download {file_name}: HTTP {response.status_code}")

            except requests.exceptions.RequestException as e:
                log_etl_error(f"Error downloading {file_name}: {e}")

except Exception as e:
    log_etl_error(f"Error while processing records: {e}")

finally:
    try:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            log_etl_success("PostgreSQL connection is closed.")
    except Exception as e:
        log_etl_error(f"Error closing PostgreSQL connection: {e}")