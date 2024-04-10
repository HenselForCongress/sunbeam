# hydrogen/utils/logging.py
import logging
import os

LOGGER_NAME = "Hydrogen☀️🪵"

# Initialize the logger
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)  # Default level

def configure_logger():
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_verbose = os.environ.get("LOG_VERBOSE", "False").lower() == "true"

    # Set up logger with new configuration
    logger.setLevel(level)

    if log_verbose:
        fmt_stream = "%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
        datefmt = '%Y-%m-%d %H:%M:%S'
    else:
        fmt_stream = " %(levelname)-8s %(message)s"
        datefmt = None

    formatter = logging.Formatter(fmt_stream, datefmt=datefmt)

    # Clear existing handlers
    logger.handlers.clear()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Make sure to test and reconfigure logger immediately, so subsequent log messages will use the new configuration
configure_logger()

def test_logger():
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
