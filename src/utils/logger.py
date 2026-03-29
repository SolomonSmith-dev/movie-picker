"""Logging utilities for MoviePicker application."""

import logging
import sys
from typing import Optional

from .config import settings, get_log_file_path


def setup_logger(
    name: str = "moviepicker",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Set up a logger with console and file handlers."""

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level or settings.log_level))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_path = get_log_file_path(log_file)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "moviepicker") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


# Default logger instance
logger = get_logger()
