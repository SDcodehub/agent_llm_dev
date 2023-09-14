import os
import sys
import argparse
import logging

# Add the root directory to sys.path to enable imports from the "tools" package
root = os.path.dirname(__file__)
sys.path.append(root)

# Import specific functions from the "tools" package
from tools.argparse_utils import parse_arguments
from tools.logging_utils import setup_logger
from tools.api_key_check import check_api_key
from tools.config_utils import get_config_paths

from chat_setup.directory_structure import DirectoryStructure


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Create an instance of the DirectoryStructure class
    directory_structure = DirectoryStructure(args.app_name)

    # Create the directory structure
    directory_structure.create_structure()

    # Now you can use these directory paths
    log_file_path = directory_structure.get_logs_directory()
    # code_file_path = os.path.join(directory_structure.get_codes_directory(), "my_code.py")
    # config_file_path = os.path.join(directory_structure.get_configs_directory(), "my_config.json")

    # Determine the log level based on the presence of the --debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO

    # Set up the logger with the determined log level and app_name
    logger = setup_logger(log_file_path, args.app_name, log_level)
    logger.info("Starting your app")

    app_desc = args.app_desc
    app_name = args.app_name
    model = args.model

    # Get the OpenAI API key securely
    openai_api_key = check_api_key('OPENAI_API_KEY')

    # Get the paths to the configuration files
    (
        agents_config_path,
        llm_config_path,
        taskchain_config_path,
        task_config_path,
    ) = get_config_paths()

    # Now you have the paths to the configuration files and can use them in your app logic.

    logger.info(f"{app_desc=}")
    logger.info(f"{app_name=}")
    logger.info(f"{model=}")
    logger.info(f"{agents_config_path=}")
    logger.info(f"{llm_config_path=}")
    logger.info(f"{taskchain_config_path=}")
    logger.info(f"{task_config_path=}")
    logger.info(f"{openai_api_key=}")

if __name__ == "__main__":
    main()
