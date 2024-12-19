import pandas as pd
from components.db_connection import get_db_connection
from project_logging.logging_module import log_info, log_error, log_success
from datetime import datetime

def fetch_data_from_db() -> pd.DataFrame:
    """
    Fetches data from the PostgreSQL database and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the fetched data.
    """

    try:
        conn = get_db_connection()

        # Check if the connection is open
        if conn.closed == 0:
            log_info("Connected to the PostgreSQL database.")

            mydata = conn.cursor()
            mydata.execute("SELECT * FROM gaia_metadata_tbl")

            result = mydata.fetchall()
            log_success("Data fetched from gaia_metadata_tbl successfully.")

            columns = [desc[0] for desc in mydata.description]
            df = pd.DataFrame(result, columns=columns)

            return df
    except Exception as e:
        log_error(f"An error occurred while fetching data from the database. Details: {e}")
        return None
    finally:
        try:
            if conn and conn.closed == 0:
                mydata.close()
                conn.close()
                log_info("PostgreSQL connection closed.")
        except Exception as e:
            log_error(f"An error occurred while closing the database connection. Details: {e}")


def fetch_data_from_db_dashboards() -> pd.DataFrame:
    """
    Fetches data from the 'model_response' table in the PostgreSQL database 
    and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the data fetched from 'model_response',
        or None if an error occurs.
    """
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()

        if conn.is_connected():
            log_success("Connected to the PostgreSQL database for dashboards.")

            # Create a cursor for dashboards
            mydata_dashboard = conn.cursor()

            # Execute SQL Query
            mydata_dashboard.execute("SELECT * FROM model_response")

            # Fetch all results
            result = mydata_dashboard.fetchall()

            # Extract column names from the cursor
            columns = [desc[0] for desc in mydata_dashboard.description]

            # Store the fetched data into a pandas DataFrame
            df_dashboards = pd.DataFrame(result, columns=columns)

            log_success("Data fetched successfully from the 'model_response' table.")
            return df_dashboards

    except Exception as e:
        log_error(f"An error occurred while fetching data: {e}")
        return None

    finally:
        # Ensure cleanup of resources
        try:
            if conn.is_connected():
                mydata_dashboard.close()
                conn.close()
                log_info("PostgreSQL connection closed for dashboards.")
        except Exception as e:
            log_error(f"Error closing the PostgreSQL connection: {e}")



def insert_model_response(
    task_id: str, date: datetime, model_used: str, model_response: str, response_category: str,
    created_at: datetime = datetime.now(), created_by: str = 'streamlit user'
) -> None:
    """
    Inserts a new record into the 'model_response' table in PostgreSQL.

    Args:
        task_id (str): Unique task identifier.
        date (datetime): Task creation or processing date.
        model_used (str): Model used (e.g., GPT-4).
        model_response (str): Generated response.
        response_category (str): Response type/category.
        created_at (datetime, optional): Record creation timestamp (default: now).
        created_by (str, optional): Record creator (default: 'streamlit user').

    Returns:
        None
    """
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()

        if conn.is_connected():
            log_success("Connected to PostgreSQL for model response insertion.")

            # Create a cursor
            cursor = conn.cursor()

            # Define the INSERT SQL query
            insert_query = """
            INSERT INTO model_response (
                task_id, date, model_used, model_response, response_category, created_at, created_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the query with provided values
            cursor.execute(
                insert_query, 
                (task_id, date, model_used, model_response, response_category, created_at, created_by)
            )

            # Commit the transaction
            conn.commit()
            log_success(f"Record inserted successfully for task_id {task_id}")

    except Exception as e:
        # Catch and log any database or execution errors
        log_error(f"Database Error while inserting model response: {e}")

    finally:
        # Cleanup: Ensure resources are closed
        try:
            if conn.is_connected():
                cursor.close()
                conn.close()
                log_info("PostgreSQL connection closed.")
        except Exception as e:
            log_error(f"Error closing PostgreSQL connection: {e}")