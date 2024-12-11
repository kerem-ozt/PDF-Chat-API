import logging
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

logger = logging.getLogger("pdf_chat")
logger.setLevel(logging.INFO)

formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

rotating_file_handler = RotatingFileHandler(
    APP_LOG_FILE, 
    maxBytes=5*1024*1024,  
    backupCount=5          
)
rotating_file_handler.setLevel(logging.INFO)
rotating_file_handler.setFormatter(formatter)

error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(console_handler)
logger.addHandler(rotating_file_handler)
logger.addHandler(error_file_handler)
