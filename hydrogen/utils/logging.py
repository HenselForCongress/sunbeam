# hydrogen/utils/logging.py
import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import json

LOGGER_NAME = "Hydrogen☀️🪵"
UNFUN_LOGGER_NAME = "Hydrogen"

# Initialize the logger
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)  # Default level

def configure_logger():
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_verbose = os.environ.get("LOG_VERBOSE", "False").lower() == "true"
    log_files = os.environ.get("LOG_FILES", "False").lower() == "true"

    # Set up logger with new configuration
    logger.setLevel(level)

    if log_verbose:
        fmt_stream = "%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
        datefmt = '%Y-%m-%d %H:%M:%S'
    else:
        fmt_stream = "%(levelname)-8s %(message)s"
        datefmt = None

    shell_handler = logging.StreamHandler()
    shell_handler.setLevel(level)
    shell_formatter = logging.Formatter(fmt_stream, datefmt=datefmt)
    shell_handler.setFormatter(shell_formatter)

    # Clear existing handlers to prevent duplication
    logger.handlers = []

    # Add handlers to logger
    logger.addHandler(shell_handler)

    # File logging configuration
    if log_files:
        # Create the logs directory if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")

        filename = f"logs/{UNFUN_LOGGER_NAME}-{time.strftime('%Y-%m-%d')}.log"

        # Formatters
        json_formatter = logging.Formatter(json.dumps({
            "time": "%(asctime)s.%(msecs)03d",
            "level": "%(levelname)-8s",
            "file": "%(filename)s",
            "function": "%(funcName)s",
            "line": "%(lineno)d",
            "message": "%(message)s"
        }), datefmt=datefmt)

        # Timed Rotating File Handler
        timed_file_handler = TimedRotatingFileHandler(filename=filename, when="midnight", interval=1, backupCount=30)
        timed_file_handler.setLevel(level)
        timed_file_handler.setFormatter(json_formatter)

        # Size-based Rotating File Handler
        size_file_handler = RotatingFileHandler(filename=filename, maxBytes=5*1024*1024, backupCount=3)  # 5MB per file
        size_file_handler.setLevel(level)
        size_file_handler.setFormatter(json_formatter)

        # Add file handlers to logger
        logger.addHandler(timed_file_handler)
        logger.addHandler(size_file_handler)

def log_exception(exc_type, exc_value, exc_traceback):
    """
    Logs an exception with its traceback.
    """
    logger.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

def test_logger():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

# Log statements for testing purposes
if __name__ == "__main__":
    import sys
    sys.excepthook = log_exception

    # Ensure logger is configured before testing it
    configure_logger()
    test_logger()
