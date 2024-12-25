from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.append('/Users/akhil/Desktop/projects-akhil/BigDataSystems/automate-extraction/')

from scripts.setup_db import setup_db
from scripts.login_hf import login_hf
from scripts.process_dataset import process_dataset
from scripts.df_to_sql import df_to_sql
from utils.config import DATABSE_CONFIG as db_conf
from utils.logging_module import log_info, log_success, log_warning, log_error, log_critical

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gaia_dataset_pipeline',
    default_args=default_args,
    description='A DAG to process GAIA dataset',
    schedule_interval=None,
    start_date=datetime(2024, 12, 1),
    catchup=False,
    )

setup_db_task = PythonOperator(
    task_id='setup_db', 
    python_callable=setup_db,
    dag=dag,
)

login_hf_task = PythonOperator(
    task_id='login_hf',
    python_callable=login_hf,
    dag=dag,
)

process_dataset_task = PythonOperator(
    task_id='process_dataset',
    python_callable=process_dataset,
    dag=dag,
)

def df_to_sql_task():
    schema = 'assignment2'
    table_name = 'gaia_dataset_tbl'
    db_config = db_conf
    dataframe_path = "utils/data/gaia_dataset.csv"
    df_to_sql(dataframe_path, schema, table_name, db_config)

load_to_sql_task = PythonOperator(
    task_id='load_to_sql',
    python_callable=df_to_sql_task,
    dag=dag,
)


setup_db_task >> login_hf_task >> process_dataset_task >> load_to_sql_task