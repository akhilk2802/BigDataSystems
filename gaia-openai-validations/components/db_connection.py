import os
import psycopg2
from psycopg2 import sql, OperationalError
from project_logging import logging_module
from dotenv import load_dotenv

load_dotenv()

aws_rds_host = os.getenv('AWS_RDS_HOST')
aws_rds_user = os.getenv('AWS_RDS_USERNAME')
aws_rds_password = os.getenv('AWS_RDS_PASSWORD')
aws_rds_port = os.getenv('AWS_RDS_DB_PORT', '5432')
aws_rds_database = os.getenv('AWS_RDS_DATABASE')


def get_db_connection():
    """
    Establishes and returns a connection to the AWS RDS PostgreSQL database using provided credentials.

    Returns:
        psycopg2 connection object: A PostgreSQL database connection object.
    """

    if not all([aws_rds_host, aws_rds_user, aws_rds_password, aws_rds_database]):
        raise ValueError("[ERROR]: Missing required environment variables. Check .env configuration.")

    try:
        conn = psycopg2.connect(
            host=aws_rds_host,
            user=aws_rds_user,
            password=aws_rds_password,
            port=aws_rds_port,
            dbname=aws_rds_database
        )
        logging_module.log_success("PostgreSQL connection established.")
        print("[SUCCESS]: PostgreSQL connection established.")
        return conn

    except OperationalError as e:
        logging_module.log_error(f"Unable to connect to the PostgreSQL database. Details: {e}")
        print(f"[ERROR]: Unable to connect to the PostgreSQL database. Details: {e}")
        raise