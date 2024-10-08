import json
from prompt_config.promptformatter import SystemMessageFormatter
from chat.openai_chat_bot import OpenAIChatBot
from chat.nvidia_chat_bot import NVIDIAChatBot
from postprocess.code_output_parser import TaskParser
from postprocess.codefile_creator import CodeFileGenerator
from prompt_config.taskconfig_formater import DynamicTaskConfigFormatter
from prompt_config.task_config_vars import IntermediateVars
from llms.openai_llm import ChatGPTConfig
from utils.config_utils import get_config_paths
from dataclasses import dataclass

@dataclass
class TaskConfig:
    assistant_role_name: str
    user_role_name: str
    phase_prompt: list[str]


class AgentConversation:
    def __init__(self, app_name, model, app_desc, logger, code_file_path, openai, nvidiaai):
        self.app_name = app_name
        self.model = model
        self.app_desc = app_desc
        self.logger = logger
        self.system_formatter = self.setup_system_formatter()
        self.openai = openai
        self.nvidiaai = nvidiaai
        self.chat_bot = self.setup_chat_bot()
        self.company_prompt = "Welcome to SmartAgents"
        self.intermediate_vars = IntermediateVars()
        self.code_file_path = code_file_path



    def setup_system_formatter(self):
        agents_config_path, _, _, _, _ = get_config_paths()
        return SystemMessageFormatter(agents_config_path)

    def setup_chat_bot(self):
        if self.openai:
            return OpenAIChatBot(
                model=self.model,
                chat_config=ChatGPTConfig.load_from_file("llmconfig.json")
            )
        if self.nvidiaai:
            return NVIDIAChatBot(
                model=self.model,
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
        phase_prompt_str = dynamic_formatter.format_task_config(assistant_role_name, phase_prompt)
        self.logger.debug(f'{phase_prompt_str=}')

        # Add the concatenated phase_prompt to assistant_messages
        assistant_system_message.user(phase_prompt_str)
        self.logger.debug(f'{assistant_system_message.messages=}')

        self.logger.info(f"User {user_role_name}: {phase_prompt_str}")

        # # Conduct the conversation by alternating between assistant and user messages
        # conversation = []

        # TODO add way to process the taskchainconfig file an get cyclenum
        if task_name == "Coding":
            cyclenum = 2
        else:
            cyclenum = 5

        for count in range(cyclenum):  # Maximum of 4 back-and-forth exchanges
            # Assistant's turn
            assistant_response = self.chat_bot.send_messages_and_get_response(
                assistant_system_message.messages
            )
            assistant_system_message.assistant(assistant_response)
            user_system_message.user(assistant_response)

            last_conv = assistant_response
            self.logger.info(f"Assistant {assistant_role_name}: {assistant_response}")

            # Check if the assistant's response starts with "<INFO>" to terminate the conversation
            if assistant_response.strip().startswith("<INFO>"):
                break
            elif task_name == "Coding" and count == cyclenum-1:
                break

            # User's turn
            user_response = self.chat_bot.send_messages_and_get_response(
                user_system_message.messages
            )
            user_system_message.assistant(user_response)
            assistant_system_message.user(user_response)

            last_conv = assistant_response
            self.logger.info(f"User {user_role_name}: {user_response}")

            # Check if the user's response starts with "<INFO>" to terminate the conversation
            if user_response.strip().startswith("<INFO>"):
                break

        # TODO parse the data output final call and add return it, add some post processing

        if task_name == "DemandAnalysis":

            parser = TaskParser(task_name, last_conv)
            output = parser.parse_output()

            self.intermediate_vars.modality = output
        elif task_name == "LanguageChoose":

            parser = TaskParser(task_name, last_conv)
            output = parser.parse_output()

            self.intermediate_vars.language = output
        elif task_name == "Coding":
            # Split the string at "####"
            split_string = last_conv.split("####")

            # Remove leading and trailing whitespace from each part
            split_string = [part.strip() for part in split_string]

            # Remove empty strings from the result
            split_string = [part for part in split_string if part]
            entire_code = ''
            for code_string in split_string:
                try:
                    parser = TaskParser(task_name, code_string)
                    filename, extension, language, docstring, code = parser.parse_output()

                    generator = CodeFileGenerator(filename, extension, language, docstring, code, self.code_file_path)
                    generator.create_code_file()

                    # filename, extension, language, docstring, code = output

                    entire_code = entire_code + filename + '\n\n' + extension + '\n\n' +  language + '\n\n' +  docstring + '\n\n' + code

                except Exception as e:
                    self.logger.error(f"Parsing the output: {str(e)}")
            self.intermediate_vars.codes = entire_code

            self.logger.info("Done")
        else:
            pass
        # return conversation


def task_config_decorator(func):
    def wrapper(self, *args, **kwargs):
        task_configs = self.get_task_configs()
        for task_name, task_config in task_configs.items():
            func(self, task_name, task_config)
    return wrapper


class AgentConversationExtended(AgentConversation):
    def __init__(self, app_name, model, app_desc, logger, task_config_path, code_file_path, openai=None, nvidiaai=None):
        super().__init__(app_name, model, app_desc, logger, code_file_path, openai=openai, nvidiaai=nvidiaai)
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
