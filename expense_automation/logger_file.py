import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger(logger_name):
    """
    Configures and returns a logger instance with a specified name.
    Ensures no duplicate handlers are added and properly closes previous handlers.
    """
    logger = logging.getLogger(logger_name)

    # Close and remove existing handlers before adding a new one
    if logger.hasHandlers():
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(log_dir, "expense_log.log")
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt='Date and Time: %(asctime)s - %(levelname)s - %(name)s - Line number: %(lineno)d : %(message)s',
        datefmt='%d-%b-%y %I:%M:%S %p'
    )

    file_handler = RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    return logger

# Suppress noisy logs
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)

# ✅ Create a default logger instance
logger = get_logger("expense_logger")
