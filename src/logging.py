import json
import logging
from logging import Formatter, LogRecord
from logging.handlers import TimedRotatingFileHandler

from src.config import settings


class JSONFormatter(Formatter):
    """Formats log events to a JSON string"""

    def format(self, record: LogRecord) -> str:
        json_record = {
            "timestamp": int(record.created),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "user_id": str(getattr(record, "user_id", None)),
            "key_id": str(getattr(record, "key_id", None)),
        }
        return json.dumps(json_record)


def get_logger(
    name: str = "default", log_file: str = settings.LOG_FILE_PATH
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.hasHandlers():
        return logger

    formatter = JSONFormatter()

    # 1. Console Handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Weekly Rotating File Handler
    # when="W0" rotates every Monday at midnight (W0 = Monday, W1 = Tuesday, etc.)
    # Use when="D" and interval=7 to rotate every 7 days from setup instead.
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="W0",
        interval=1,
        backupCount=4,  # Retains 4 weeks of backlogs before deleting
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
