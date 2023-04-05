import logging
import logging.handlers
from pathlib import Path
from typing import Union

from waffle_utils.file import io

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
MAX_BYTES = 1024 * 50  # for RotatingFileHandler
BACKUP_COUNT = 20

DEFAULT_ROOT_LEVEL = logging.DEBUG
DEFAULT_CONSOLE_LEVEL = logging.INFO
DEFAULT_FILE_LEVEL = logging.DEBUG

DEFAULT_TIMED_ROATETING_WHEN = "D"
DEFAULT_TIMED_ROATETING_INTERVAL = 1
DEFAULT_ENCODING = "utf8"


class LogLevel:
    "One of logging Levels"


def initialize_logger(
    file_path: Union[str, Path],
    console_level: LogLevel = DEFAULT_CONSOLE_LEVEL,
    file_level: LogLevel = DEFAULT_FILE_LEVEL,
    root_level: LogLevel = DEFAULT_ROOT_LEVEL,
):

    # Create the log folder for the log file
    file_path = Path(file_path)
    io.make_directory(file_path.parent)

    # Define the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)

    # Define the formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # Define the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # Define the file handler
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(file_path),
        when=DEFAULT_TIMED_ROATETING_WHEN,
        interval=DEFAULT_TIMED_ROATETING_INTERVAL,
        backupCount=BACKUP_COUNT,
        encoding=DEFAULT_ENCODING,
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # Add Handler
    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
