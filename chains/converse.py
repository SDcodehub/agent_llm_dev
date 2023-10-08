from prompt_config.promptformatter import SystemMessageFormatter
from chat.openai_chat_bot import OpenAIChatBot
from prompt_config.taskconfig_formater import DynamicTaskConfigFormatter
from prompt_config.task_config_vars import IntermediateVars
from utils.logging_utils import setup_logger
from chat.message import Message
from llms.openai_llm import ChatGPTConfig
from utils.config_utils import get_config_paths
from utils.api_key_check import check_api_key
import logging
import json
from dataclasses import dataclass

@dataclass
class TaskConfig:
    assistant_role_name: str
    user_role_name: str
    phase_prompt: list[str]


class AgentConversation:
    def __init__(self, app_name, model, app_desc, logger):
        self.app_name = app_name
        self.model = model
        self.app_desc = app_desc
        self.logger = logger
        self.system_formatter = self.setup_system_formatter()
        self.openai_api_key = check_api_key('OPENAI_API_KEY')
        self.chat_bot = self.setup_chat_bot()
        self.company_prompt = "Welcome to SmartAgents"
        self.intermediate_vars = IntermediateVars()
        print(self.intermediate_vars)


    def setup_system_formatter(self):
        agents_config_path, _, _, _ = get_config_paths()
        return SystemMessageFormatter(agents_config_path)

    def setup_chat_bot(self):
        return OpenAIChatBot(
            model=self.model,
            api_key=self.openai_api_key,
            chat_config=ChatGPTConfig.load_from_file("llmconfig.json")
        )

    def create_conversation(self, task_name, task_config):
        user_role_name = task_config.user_role_name
        assistant_role_name = task_config.assistant_role_name
        phase_prompt = task_config.phase_prompt

        self.logger.info("-" * 5 + task_name + "-" * 5)

        # Generate system messages for the user and assistant based on their roles
        user_system_message = self.system_formatter.format_message(
            user_role_name, self.company_prompt, self.app_desc
        )

        assistant_system_message = self.system_formatter.format_message(
            assistant_role_name, self.company_prompt, self.app_desc
        )

        self.logger.debug(f'{user_system_message.messages=}')

        # Add data from the task to the IntermediateVars instance
        self.intermediate_vars.task = task_name

        # Create a new DynamicTaskConfigFormatter for each task
        dynamic_formatter = DynamicTaskConfigFormatter(self.intermediate_vars)

        # Use the dynamic formatter to format the task_config
        phase_prompt_str = self.dynamic_formatter.format_task_config(assistant_role_name, phase_prompt)
        self.logger.debug(f'{phase_prompt_str=}')

        # Add the concatenated phase_prompt to assistant_messages
        assistant_system_message.user(phase_prompt_str)
        self.logger.debug(f'{assistant_system_message.messages=}')

        self.logger.info(f"User {user_role_name}: {phase_prompt_str}")

        # # Conduct the conversation by alternating between assistant and user messages
        # conversation = []

        for _ in range(4):  # Maximum of 4 back-and-forth exchanges
            # Assistant's turn
            assistant_response = self.chat_bot.send_messages_and_get_response(
                assistant_system_message.messages
            )
            assistant_system_message.assistant(assistant_response)
            user_system_message.user(assistant_response)

            self.logger.info(f"Assistant {assistant_role_name}: {assistant_response}")

            # Check if the assistant's response starts with "<INFO>" to terminate the conversation
            if assistant_response.strip().startswith("<INFO>"):
                break

            # User's turn
            user_response = self.chat_bot.send_messages_and_get_response(
                user_system_message.messages
            )
            user_system_message.assistant(user_response)
            assistant_system_message.user(user_response)

            self.logger.info(f"User {user_role_name}: {user_response}")

            # Check if the user's response starts with "<INFO>" to terminate the conversation
            if user_response.strip().startswith("<INFO>"):
                break

        # TODO parse the data output final call and add return it, add some post processing
        # return conversation


def task_config_decorator(func):
    def wrapper(self, *args, **kwargs):
        task_configs = self.get_task_configs()
        for task_name, task_config in task_configs.items():
            conversation = func(self, task_name, task_config)
            # TODO Need update to task_config_vars dataclass post execution of the conversation
    return wrapper


class AgentConversationExtended(AgentConversation):
    def __init__(self, app_name, model, app_desc, logger, task_config_path):
        super().__init__(app_name, model, app_desc, logger)
        self.task_config_path = task_config_path

    def get_task_configs(self):
        task_configs = {}
        try:
            # Use the provided task_config_path to load the TaskConfig.json file
            with open(self.task_config_path, "r", encoding="utf-8") as config_file:
                config_data = json.load(config_file)

            # Iterate through the task configurations and create TaskConfig objects
            for task_name, task_data in config_data.items():
                if "assistant_role_name" in task_data and "user_role_name" in task_data and "phase_prompt" in task_data:
                    task_config = TaskConfig(
                        assistant_role_name=task_data["assistant_role_name"],
                        user_role_name=task_data["user_role_name"],
                        phase_prompt=task_data["phase_prompt"]
                    )
                    task_configs[task_name] = task_config

        except FileNotFoundError:
            self.logger.error("TaskConfig.json file not found.")
        except Exception as e:
            self.logger.error(f"Error reading TaskConfig.json: {str(e)}")

        return task_configs

    @task_config_decorator
    def run_conversations(self, task_name, task_config):
        return self.create_conversation(task_name, task_config)


    def print_conversation(self, conversation):
        # Print the conversation
        for exchange in conversation:
            self.logger.info(f"User: {exchange['User']}")
            self.logger.info(f"Assistant: {exchange['Assistant']}")


if __name__ == "__main__":
    app_name = "YourAppName"
    model = "YourModelName"
    app_desc = "YourAppDescription"

    conversation_manager = AgentConversationExtended(app_name, model, app_desc)
    conversation_manager.run_conversations()
