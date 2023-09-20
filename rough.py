from typing import Dict, Optional
from message import Message

class TaskPromptFormatter:
    def __init__(self, task_config: Dict):
        """
        Initialize the TaskPromptFormatter with task configuration.

        Args:
            task_config (Dict): Configuration for the task.

        Attributes:
            task_config (Dict): Configuration for the task.
        """
        self.task_config = task_config

    def get_task_prompts(self, task_name: str) -> Optional[List[str]]:
        """
        Get the task-specific prompts for a given task name.

        Args:
            task_name (str): The name of the task.

        Returns:
            Optional[List[str]]: A list of formatted task prompts if found, None otherwise.
        """
        task_info = self.task_config.get(task_name)
        if task_info:
            return task_info.get("phase_prompt", None)
        return None

class RoleSystemMessageFormatter:
    def __init__(self, agents_config: Dict):
        """
        Initialize the RoleSystemMessageFormatter with agents configuration.

        Args:
            agents_config (Dict): Configuration for the agents.

        Attributes:
            agents_config (Dict): Configuration for the agents.
        """
        self.agents_config = agents_config

    def get_system_message(self, agent_name: str, task_name: str) -> str:
        """
        Get the system message for an agent based on the agent name and task name.

        Args:
            agent_name (str): The name of the agent.
            task_name (str): The name of the task.

        Returns:
            str: The formatted system message.
        """
        agent_prompts = self.agents_config.get(agent_name, [])
        system_message = ""

        # Find the system message for the specified agent
        for prompt_line in agent_prompts:
            if "{task}" in prompt_line:
                system_message = prompt_line.replace("{task}", task_name)
                break

        return system_message

class ConversationBuilder:
    def __init__(self, task_config: Dict, agents_config: Dict):
        # Initialize with task and agents configurations as before
        self.task_config = task_config
        self.agents_config = agents_config

    def build_user_and_assistant(self, task_name: str, assistant_role: str, chatdev_prompt: Optional[str] = None):
        """
        Build instances of user and assistant OpenAIChatBot classes with system messages.

        Args:
            task_name (str): The name of the task.
            assistant_role (str): The role of the assistant.
            chatdev_prompt (Optional[str]): A custom ChatDev prompt.

        Returns:
            Tuple[OpenAIChatBot, OpenAIChatBot]: A tuple containing user and assistant instances.
        """
        # Initialize user and assistant instances
        user = self._init_openai_chat_bot("gpt-3.5-turbo", api_key="user_api_key")
        assistant = self._init_openai_chat_bot("gpt-3.5-turbo", api_key="assistant_api_key")

        # Get the user and assistant system messages
        user_system_message = self._get_user_system_message(task_name)
        assistant_system_message = self._get_assistant_system_message(assistant_role, task_name)

        # Set system messages for user and assistant
        user.system_message(user_system_message)
        assistant.system_message(assistant_system_message)

        # Build a conversation and set it as the first message for the assistant
        assistant_conversation = self.build_conversation(task_name, assistant_role, chatdev_prompt)
        assistant.messages = assistant_conversation.messages

        return user, assistant

    def _init_openai_chat_bot(self, model: str, api_key: str) -> OpenAIChatBot:
        """
        Initialize an OpenAIChatBot instance with the given model and API key.

        Args:
            model (str): The name of the GPT model.
            api_key (str): The API key for authentication.

        Returns:
            OpenAIChatBot: An instance of OpenAIChatBot.
        """
        bot = OpenAIChatBot(model, api_key=api_key)
        return bot

    def _get_user_system_message(self, task_name: str) -> str:
        """
        Get the system message for the user based on the task name.

        Args:
            task_name (str): The name of the task.

        Returns:
            str: The formatted system message for the user.
        """
        return f"User System Message for Task: {task_name}"

    def _get_assistant_system_message(self, assistant_role: str, task_name: str) -> str:
        """
        Get the system message for the assistant based on the assistant role and task name.

        Args:
            assistant_role (str): The role of the assistant.
            task_name (str): The name of the task.

        Returns:
            str: The formatted system message for the assistant.
        """
        return f"Assistant System Message for Role: {assistant_role}, Task: {task_name}"

class OpenAIChatBot:
    # ... (OpenAIChatBot class as before)
