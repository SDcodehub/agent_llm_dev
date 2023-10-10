# Import utils
from utils.argparse_utils import parse_arguments
from utils.logging_utils import setup_logger
from utils.api_key_check import check_api_key
from utils.config_utils import get_config_paths
from chains.converse import AgentConversationExtended

from prompt_config.promptformatter import AgentMessageFormatter, SystemMessageFormatter

from llms.openai_llm import ChatGPTConfig
from chat.openai_chat_bot import OpenAIChatBot

from chat.message import Message

from setup.directory_structure import DirectoryStructure

import os
import sys
import logging

# Add the root directory to sys.path to enable imports from the "utils" package
root = os.path.dirname(__file__)
sys.path.append(root)


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Create an instance of the DirectoryStructure class
    directory_structure = DirectoryStructure(args.app_name)

    # Create the directory structure
    directory_structure.create_structure()

    # Now you can use these directory paths
    log_file_path = directory_structure.get_logs_directory()
    code_file_path = directory_structure.get_codes_directory()
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

    logger.info(f"{app_desc=}")
    logger.info(f"{app_name=}")
    logger.info(f"{model=}")
    logger.info(f"{agents_config_path=}")
    logger.info(f"{llm_config_path=}")
    logger.info(f"{taskchain_config_path=}")
    logger.info(f"{task_config_path=}")

    # Create an instance of the AgentConversationExtended class
    conversation_manager = AgentConversationExtended(app_name, model, app_desc, logger, task_config_path, code_file_path)

    # Run conversations for all tasks using the decorator
    conversation_manager.run_conversations()


if __name__ == "__main__":
    main()
