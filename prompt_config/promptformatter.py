import json
from typing import Optional
from chat.message import Message


class AgentMessageFormatter:
    def __init__(self, agents_config_path: str):
        self.agents_config_path = agents_config_path
        self.load_agents_config()

    def load_agents_config(self):
        """
        Load the agentsconfig file into a dictionary.
        """
        with open(self.agents_config_path, 'r') as config_file:
            self.agents_config = json.load(config_file)

    def format_message(self, agent_role: str, company_prompt: str, task: str) -> str:
        """
        Format and return a message based on agent's role, company prompt, and task.

        Args:
            agent_role (str): The role of the agent.
            company_prompt (str): The company prompt.
            task (str): The task description.

        Returns:
            str: The formatted message.
        """
        if agent_role in self.agents_config:
            agent_info = self.agents_config[agent_role]
            formatted_message = '\n'.join(agent_info).format(company_prompt=company_prompt, task=task)
            return formatted_message
        else:
            return "Agent role not found in configuration"


class SystemMessageFormatter(AgentMessageFormatter):
    def __init__(self, agents_config_path: str):
        super().__init__(agents_config_path)

    def format_message(self, agent_role: str, company_prompt: str, task: str) -> str:
        """
        Format and return a system message based on agent's role, company prompt, and task.

        Args:
            agent_role (str): The role of the agent.
            company_prompt (str): The company prompt.
            task (str): The task description.

        Returns:
            str: The formatted system message.
        """
        message = Message()
        message.system(super().format_message(agent_role, company_prompt, task))
        return message


# class TaskMessageFormatter(AgentMessageFormatter):
#     def __init__(self, agents_config_path: str):
#         super().__init__(agents_config_path)
#
#     def format_message(self, agent_role: str) -> str:
#         """
#         Format and return a system message based on agent's role, company prompt, and task.
#
#         Args:
#             agent_role (str): The role of the agent.
#             company_prompt (str): The company prompt.
#             task (str): The task description.
#
#         Returns:
#             str: The formatted system message.
#         """
#         message = Message()
#         message.system(super().format_message(agent_role))
#         return message


if __name__ == "__main__":
    # Define the path to the agentsconfig file
    agents_config_path = 'agentsconfig.json'

    # Create an instance of the SystemMessageFormatter
    system_formatter = SystemMessageFormatter(agents_config_path)

    # Example usage for generating a system message for an agent role
    agent_role = "Chief Executive Officer"
    company_prompt = "Welcome to ChatDev"
    task = "Develop a new software feature"
    system_message = system_formatter.format_message(agent_role, company_prompt, task)
    print(system_message.messages)
