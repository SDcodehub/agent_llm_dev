import logging
import os
from datetime import datetime

def setup_logger(app_name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger for the application.

    Args:
        app_name (str): The name of the application.
        log_level (int): The log level for the logger.

    Returns:
        logging.Logger: The configured logger.
    """
    # Create a directory for logs if it doesn't exist
    log_dir = os.path.join("outputs", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Generate a unique log file name based on app_name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file = os.path.join(log_dir, f"{app_name}_{timestamp}.log")

    logger = logging.getLogger(app_name)  # Changed logger name to app_name
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

    return logger
