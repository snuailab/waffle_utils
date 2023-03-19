import logging
import logging.handlers
from pathlib import Path
from typing import Union


class CustomLogger:
    def __init__(
        self,
        file_path: Union[str, Path] = "logs/waffle.log",
    ):

        # Create the log folder for the log file
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

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
            filename=str(file_path),
            maxBytes=1024 * 50,  # 50 MB
            backupCount=20,
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Define the root logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Add the handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
