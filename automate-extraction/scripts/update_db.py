import psycopg2
from utils.logging_module import log_info, log_error
from utils.config import DATABSE_CONFIG
from utils.config import AWS_CONFIG

def update_database():
    try:
        connection = psycopg2.connect(**DATABSE_CONFIG)
        cursor = connection.cursor()

        # Fetch records with PDFs
        cursor.execute("SELECT * FROM assignment2.gaia_dataset_tbl WHERE file_extension = 'pdf'")
        records = cursor.fetchall()

        for record in records:
            file_name = record['file_name']
            base_name = file_name.split('.')[0]

            # Construct S3 URLs for both PyPDF and Unstructured outputs
            s3_url_pypdf = f"https://{AWS_CONFIG['s3_bucket']}.s3.amazonaws.com/extracted_text/pypdf/{base_name}.json"
            s3_url_unstructured = f"https://{AWS_CONFIG['s3_bucket']}.s3.amazonaws.com/extracted_text/unstructured/{base_name}.json"

            # Update the database with the respective URLs
            update_query = """
                UPDATE assignment2.gaia_dataset_tbl
                SET s3_url_extracted_pypdf = %s,
                    s3_url_extracted_unstructured = %s
                WHERE task_id = %s
            """
            cursor.execute(update_query, (s3_url_pypdf, s3_url_unstructured, record['task_id']))
            connection.commit()

        cursor.close()
        connection.close()
        log_info("Database updated successfully with extracted text info.")
    except Exception as e:
        log_error(f"Error in update_database: {e}")
        raise