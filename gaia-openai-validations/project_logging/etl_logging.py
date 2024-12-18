# etl_logging.py - ETL Logs Setup
import logging
from datetime import datetime
import os

# Create Log Directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ETL Log File Setup
ETL_LOG_FILE = os.path.join(LOG_DIR, f"etl_log_{datetime.now().strftime('%Y%m%d')}.log")

# Configure Logging for ETL
etl_logger = logging.getLogger("etl_logger")
etl_logger.setLevel(logging.INFO)

# File Handler for ETL Logs
etl_file_handler = logging.FileHandler(ETL_LOG_FILE)
etl_file_handler.setLevel(logging.INFO)

# Formatter for ETL Logs
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
etl_file_handler.setFormatter(formatter)

# Add the File Handler to ETL Logger
etl_logger.addHandler(etl_file_handler)

# Define Custom Log Functions for ETL
def log_etl_info(message: str):
    etl_logger.info(message)
    print(f"[ETL INFO]: {message}")

def log_etl_success(message: str):
    etl_logger.info(f"ETL SUCCESS: {message}")
    print(f"[ETL SUCCESS]: {message}")

def log_etl_warning(message: str):
    etl_logger.warning(message)
    print(f"[ETL WARNING]: {message}")

def log_etl_error(message: str):
    etl_logger.error(message)
    print(f"[ETL ERROR]: {message}")

def log_etl_critical(message: str):
    etl_logger.critical(message)
    print(f"[ETL CRITICAL]: {message}")