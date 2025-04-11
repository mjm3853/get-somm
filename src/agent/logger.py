"""This module provides a centralized logging configuration for the application."""
import logging


def setup_logging(level=logging.INFO):
    """Set up the logging configuration for the application.

    Args:
        level: The logging level to use. Defaults to logging.INFO.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

# Call this function to initialize logging when your application starts.
