"""This module provides a centralized logging configuration for the application."""
import logging

# Expose the logger and setup_logging function for external use
__all__ = ["logger", "setup_logging"]

# Create a logger instance
logger = logging.getLogger("get-somm")
logger.setLevel(logging.INFO)

# Set up a default handler with basic configuration
default_handler = logging.StreamHandler()
default_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(default_handler)

def setup_logging(level=logging.INFO):
    """Reconfigure the logging level for the logger.

    Args:
        level: The logging level to use. Defaults to logging.INFO.
    """
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
