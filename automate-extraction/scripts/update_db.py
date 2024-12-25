import psycopg2
from utils.logging_module import log_info, log_error
from utils.config import DATABSE_CONFIG
from utils.config import AWS_CONFIG

def update_database():
    try:
        connection = psycopg2.connect(**DATABSE_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assignment2.gaia_dataset_tbl WHERE file_extension = 'pdf'")
        records = cursor.fetchall()

        for record in records:
            file_name = record['file_name']
            s3_url = f"https://{AWS_CONFIG['s3_bucket']}.s3.amazonaws.com/extracted_text/{file_name.split('.')[0]}.json"
            update_query = "UPDATE assignment2.gaia_dataset_tbl SET s3_url_extracted = %s, extraction_tool = %s WHERE task_id = %s"
            cursor.execute(update_query, (s3_url, 'PyPDF2', record['task_id']))
            connection.commit()

        cursor.close()
        connection.close()
        log_info("Database updated successfully with extracted text info")
    except Exception as e:
        log_error(f"Error in update_database: {e}")
        raise