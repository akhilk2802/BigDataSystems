from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize DAG
dag = DAG(
    'my_first_dag',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 12, 1),
    catchup=False
)

# Task 1: Print Hello
def print_hello():
    print("Hello, Airflow!")

hello_task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag
)

# Task 2: Print Date using Bash
bash_task = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag
)

# Define dependencies
hello_task >> bash_task