import logging
from datetime import datetime
import os

LOG_DIR = "general_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

GENERAL_LOG_FILE = os.path.join(LOG_DIR, f"general_log_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    filename=GENERAL_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filemode="a"
)

general_logger = logging.getLogger("general_logger")
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