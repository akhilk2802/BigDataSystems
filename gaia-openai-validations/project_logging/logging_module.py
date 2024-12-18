import logging
from datetime import datetime
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"app_log_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,                # Log everything from DEBUG level and above
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a"
)

logger = logging.getLogger()

# Define Custom Log Functions
def log_info(message: str):
    """Log informational messages."""
    logger.info(message)
    print(f"[INFO]: {message}")

def log_success(message: str):
    """Log success messages."""
    logger.info(f"SUCCESS: {message}")
    print(f"[SUCCESS]: {message}")

def log_warning(message: str):
    """Log warning messages."""
    logger.warning(message)
    print(f"[WARNING]: {message}")

def log_error(message: str):
    """Log error messages."""
    logger.error(message)
    print(f"[ERROR]: {message}")

def log_critical(message: str):
    """Log critical error messages."""
    logger.critical(message)
    print(f"[CRITICAL]: {message}")