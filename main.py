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

    logger.info(f"{app_desc=}")
    logger.info(f"{app_name=}")
    logger.info(f"{model=}")
    logger.info(f"{agents_config_path=}")
    logger.info(f"{llm_config_path=}")
    logger.info(f"{taskchain_config_path=}")
    logger.info(f"{task_config_path=}")
    logger.info(f"{openai_api_key=}")

    # Make selection of people working on project.

    # Create an instance of the AgentMessageFormatter
    # Define the path to the agentsconfig file
    # agents_config_path = agents_config_path
    #
    # # Create an instance of the SystemMessageFormatter
    # system_formatter = SystemMessageFormatter(agents_config_path)
    #
    # # Example usage for generating a system message for an agent role
    # agent_role1 = "Chief Executive Officer"
    # company_prompt1 = "Welcome to SmartAgents"
    # task = app_desc
    # system_message1 = system_formatter.format_message(agent_role1, company_prompt1, task)
    # logger.info(system_message1.messages)
    #
    # agent_role2 = "Chief Executive Officer"
    # company_prompt2 = "Welcome to SmartAgents"
    # task = app_desc
    # system_message2 = system_formatter.format_message(agent_role2, company_prompt2, task)
    # logger.info(system_message2.messages)
    #
    # # Create an OpenAIChatBot instance
    # chat_bot = OpenAIChatBot(model=model, api_key=openai_api_key,
    #                          chat_config=ChatGPTConfig.load_from_file("llmconfig.json"))
    # #
    # # # Trial 1
    # # message_1 = Message()
    # # message_1.system("You are a helpful assistant.")
    # # message_1.user("Who won the world series in 2020?")
    # # message_1.assistant("The Los Angeles Dodgers won the World Series in 2020.")
    # # message_1.user("Where was it played?")
    # #
    # # messages_1 = message_1.messages
    # logger.debug(f"{chat_bot._calculate_token_count(system_message.messages)=}")
    # response_1 = chat_bot.send_messages_and_get_response(system_message.messages)
    #
    # logger.info(f"Trial 1 - Assistant's Response: {response_1}")
    #
    #
    # # Trial 2
    # message_2 = Message()
    # message_2.system("You are an informative assistant.")
    # message_2.user("Tell me about the Eiffel Tower.")
    # message_2.assistant("The Eiffel Tower is a famous landmark in Paris, France.")
    # message_2.user("How tall is it?")
    #
    # messages_2 = message_2.messages
    # logger.debug(f"{chat_bot._calculate_token_count(messages_2)=}")
    # response_2 = chat_bot.send_messages_and_get_response(messages_2)
    #
    # logger.info(f"Trial 2 - Assistant's Response: {response_2}")
    # save files

    # Create an instance of the AgentConversationExtended class
    conversation_manager = AgentConversationExtended(app_name, model, app_desc, logger, task_config_path)

    # Run conversations for all tasks using the decorator
    conversation_manager.run_conversations()


if __name__ == "__main__":
    main()
