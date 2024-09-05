import logging
import os
from datetime import datetime
from pathlib import Path
from colorlog import ColoredFormatter


def setup_logger(log_folder: Path, app_name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger for the application.

    Args:
        log_folder (Path): The path to the folder where log files will be stored.
        app_name (str): The name of the application.
        log_level (int): The log level for the logger.

    Returns:
        logging.Logger: The configured logger.
    """

    # Generate a unique log file name based on app_name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(log_folder, f"{app_name}_{timestamp}.log")

    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    # Create a file handler to log messages to the file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a console handler to log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Define a formatter for log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log the initial timestamp
    logger.info("Logging started at %s.", timestamp)

    return logger


def setup_colored_logger(log_folder: Path, app_name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger for the application with colored output.

    Args:
        log_folder (Path): The path to the folder where log files will be stored.
        app_name (str): The name of the application.
        log_level (int): The log level for the logger.

    Returns:
        logging.Logger: The configured logger.
    """

    # Generate a unique log file name based on app_name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(log_folder, f"{app_name}_{timestamp}.log")

    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    # Create a file handler to log messages to the file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create a console handler to log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Define a formatter for log messages with colors
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log the initial timestamp
    logger.info("Logging started at %s.", timestamp)

    return logger

