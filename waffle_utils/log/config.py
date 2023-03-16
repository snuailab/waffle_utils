import logging
import logging.handlers
from pathlib import Path


def get_logger():
    # Create the log folder for the log file
    log_file_path = Path("logs/waffle.log")
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Define the formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
    )

    # Define the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Define the file handler
    file_handler = logging.handlers.RotatingFileHandler(
        filename=str(log_file_path),
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Define the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Add the handlers to the root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
