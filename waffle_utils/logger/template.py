import logging
import logging.handlers
from pathlib import Path
from typing import Union

from waffle_utils.file import io

DEFAULT_LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
)


class LogLevel:
    "One of logging Levels"


class CustomColorFormatter(logging.Formatter):
    """Custom color formatter for logging"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._colors = {
            "DEBUG": "\033[94m",
            "INFO": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[91m",
            "ENDC": "\033[0m",
        }

    def format(self, record):
        levelname = record.levelname
        msg = super().format(record)
        return f"{self._colors[levelname]}{msg}{self._colors['ENDC']}"


def initialize_logger(
    file_path: Union[str, Path] = None,
    log_format: str = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s",
    console_level: LogLevel = logging.INFO,
    file_level: LogLevel = logging.INFO,
    root_level: LogLevel = logging.INFO,
    backup_count: int = 20,
    encoding: str = "utf8",
    when: str = "D",
    interval: int = 1,
):
    """Initialize logger

    Args:
        file_path (Union[str, Path], optional): path to log file. Defaults to None.
        console_level (LogLevel, optional): log level for console. Defaults to INFO.
        file_level (LogLevel, optional): log level for file. Defaults to INFO.
        root_level (LogLevel, optional): log level for root. Defaults to INFO.
        backup_count (int, optional): backup count for log file. Defaults to 20.
        encoding (str, optional): encoding for log file. Defaults to "utf8".
        when (str, optional): when for log file. Defaults to "D".
        interval (int, optional): interval for log file. Defaults to 1.
    """
    # Define the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)

    # Define the formatter
    formatter = CustomColorFormatter(log_format)

    # Define the console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # Add Handler
    root_logger.handlers = []
    root_logger.addHandler(console_handler)

    # Define the file handler
    if file_path is not None:
        file_path = Path(file_path)
        io.make_directory(file_path.parent)
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=str(file_path),
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding,
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
