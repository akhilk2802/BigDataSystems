from utils.config import DATABSE_CONFIG as db_conf
from utils.logging_module import log_success, log_error
import psycopg2


def alter_table():
    alter_table_query = """
    ALTER TABLE assignment2.gaia_dataset_tbl
    ADD COLUMN IF NOT EXISTS s3_url VARCHAR(255),
    ADD COLUMN IF NOT EXISTS file_extension VARCHAR(255),
    ADD COLUMN IF NOT EXISTS s3_url_extracted_azure VARCHAR(255),
    ADD COLUMN IF NOT EXISTS s3_url_extracted_pypdf VARCHAR(255);
    """

    try:
        connection = psycopg2.connect(**db_conf)
        log_success("Connected to the database")
        cur = connection.cursor()
        cur.execute(alter_table_query)
        connection.commit()
        log_success("Table altered successfully")
    except Exception as e:
        log_error(f"Failed to alter table: {e}")
        raise
    finally:
        if connection:
            cur.close()
            connection.close()
            log_success("Database connection closed successfully")
