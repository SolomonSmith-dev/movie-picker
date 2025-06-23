"""MoviePicker - A smart movie recommendation and management system."""

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .utils.config import ensure_directories
from .utils.logger import setup_logger

# Ensure all required directories exist
ensure_directories()

# Set up default logger
setup_logger("moviepicker", log_file="moviepicker.log")
