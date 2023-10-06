from prompt_config.promptformatter import SystemMessageFormatter
from chat.openai_chat_bot import OpenAIChatBot
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

    # def setup_logger(self):
    #     log_file_path = f"logs/{self.app_name}"  # Adjust the log file path as needed
    #     log_level = logging.DEBUG  # You can adjust the log level here
    #     logger = setup_logger(log_file_path, self.app_name, log_level)
    #     logger.info("Starting your app")
    #     return logger

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

        # Generate system messages for the user and assistant based on their roles
        user_system_message = self.system_formatter.format_message(
            user_role_name, self.app_desc, task_name
        )
        assistant_system_message = self.system_formatter.format_message(
            assistant_role_name, self.app_desc, task_name
        )

        # Start the conversation with initial system messages
        user_messages = user_system_message.messages
        assistant_messages = assistant_system_message.messages

        # Conduct the conversation by alternating between user and assistant messages
        conversation = []
        for i in range(len(phase_prompt)):
            user_messages.append(phase_prompt[i])
            response = self.chat_bot.send_messages_and_get_response(
                user_messages + assistant_messages
            )
            assistant_messages.append(response)

            conversation.append({
                "User": user_messages[-1],
                "Assistant": response
            })

            # Terminate the conversation if it ends with "<INFO>"
            if response.strip().startswith("<INFO>"):
                break

        return conversation


def task_config_decorator(func):
    def wrapper(self, *args, **kwargs):
        task_configs = self.get_task_configs()
        for task_name, task_config in task_configs.items():
            conversation = func(self, task_name, task_config)
            self.print_conversation(conversation)
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
            print(f"User: {exchange['User']}")
            print(f"Assistant: {exchange['Assistant']}")

if __name__ == "__main__":
    app_name = "YourAppName"
    model = "YourModelName"
    app_desc = "YourAppDescription"

    conversation_manager = AgentConversationExtended(app_name, model, app_desc)
    conversation_manager.run_conversations()
