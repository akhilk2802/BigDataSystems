from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/Users/akhil/Desktop/projects-akhil/BigDataSystems/automate-extraction/')

from scripts.fetch_download_pdfs import fetch_download_pdfs
from scripts.extract_text_pypdf import extract_text_pypdf
from scripts.upload_extracted_text import upload_extracted_text
from scripts.extract_text_unstructured import extract_text_unstructured
from scripts.update_db import update_database

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_extract_gaia',
    default_args=default_args,
    description='Fetch and extract GAIA dataset',
    schedule_interval=None,
    start_date=datetime(2024, 12, 1),
    catchup=False,
)


fetch_pdfs_task = PythonOperator(
    task_id='fetch_download_pdfs',
    python_callable=fetch_download_pdfs,
    dag=dag,
)

# extract_text_task = PythonOperator(
#     task_id='text_extraction',
#     python_callable=extract_text_from_pdfs,
#     dag=dag,
# )

extract_text_pypdf_task = PythonOperator(
    task_id='extract_text_pypdf',
    python_callable=extract_text_pypdf,
    dag=dag,
)

extract_text_unstructured_task = PythonOperator(
    task_id='extract_text_unstructured',
    python_callable=extract_text_unstructured,
    dag=dag,
)

upload_extracted_text_task = PythonOperator(
    task_id='upload_extracted_text',
    python_callable=upload_extracted_text,
    dag=dag,
)

update_db_task = PythonOperator(
    task_id='update_db',
    python_callable=update_database,
    dag=dag,
)

fetch_pdfs_task >> extract_text_pypdf_task >> extract_text_unstructured_task >>upload_extracted_text_task >> update_db_task