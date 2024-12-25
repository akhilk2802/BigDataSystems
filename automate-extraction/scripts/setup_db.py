import psycopg2
# from dotenv import load_dotenv
from utils.logging_module import log_info, log_success, log_warning, log_error, log_critical
from utils.config import DATABSE_CONFIG as db_config

def setup_db():
    schema_creation_query = "CREATE SCHEMA IF NOT EXISTS assignment2;"
    try:
        connection = psycopg2.connect(**db_config)
        log_info("Connected to the database")

        cursor = connection.cursor()
        cursor.execute(schema_creation_query)
        log_success("Schema created successfully")

        connection.commit()
        log_success("Schema commited successfully")
    except Exception as e:
        log_critical("Failed to connect to the database")
        log_error(f"Error: {e}")
        raise
    finally:
        if connection:
            cursor.close()
            connection.close()
            log_success("Database connection closed successfully")