# logging_module.py - General Logs Setup
import logging
from datetime import datetime
import os

# Create Log Directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# General Log File Setup
GENERAL_LOG_FILE = os.path.join(LOG_DIR, f"general_log_{datetime.now().strftime('%Y%m%d')}.log")

# Configure Logging for General Logs
logging.basicConfig(
    filename=GENERAL_LOG_FILE,
    level=logging.INFO,  # Log everything from DEBUG level and above
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a"
)

# Create Logger
general_logger = logging.getLogger("general_logger")

# Define Custom Log Functions
def log_info(message: str):
    general_logger.info(message)
    print(f"[INFO]: {message}")

def log_success(message: str):
    general_logger.info(f"SUCCESS: {message}")
    print(f"[SUCCESS]: {message}")

def log_warning(message: str):
    general_logger.warning(message)
    print(f"[WARNING]: {message}")

def log_error(message: str):
    general_logger.error(message)
    print(f"[ERROR]: {message}")

def log_critical(message: str):
    general_logger.critical(message)
    print(f"[CRITICAL]: {message}")