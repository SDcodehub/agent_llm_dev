import sys
import os

# Get the absolute path to the project's root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

import openai
from typing import List, Dict, Union, Optional

# from ..configs import ChatGPTConfig
from llms.openai_llm import ChatGPTConfig


class OpenAIChatBot:
    """
    A class to interact with the OpenAI Chat Completions API.

    Args:
        model (str): The name of the GPT-3.5 model to use.
        api_key (str, optional): Your OpenAI API key for authentication.
        chat_config (ChatGPTConfig, optional): Configuration for the chat bot.

    Attributes:
        model (str): The name of the GPT-3.5 model.
        api_key (str): Your OpenAI API key.
        chat_config (ChatGPTConfig): Configuration for the chat bot.

    Methods:
        send_messages_and_get_response(messages: List[Dict[str, str]]) -> Union[str, Dict]:
            Sends a list of messages to the OpenAI API and returns the response.

        _get_assistant_response(messages: List[Dict[str, str]]) -> Union[str, Dict]:
            Sends messages to the OpenAI API and retrieves the response.
    """

    def __init__(self, model: str, api_key: str = None, chat_config: Optional[ChatGPTConfig] = None):
        self.model = model
        self.api_key = api_key
        self.chat_config = chat_config

    def send_messages_and_get_response(self, messages: List[Dict[str, str]]) -> Union[str, Dict]:
        """
        Sends a list of messages to the OpenAI API and returns the response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            Union[str, Dict]: The response from the OpenAI API.
        """
        try:
            response = self._get_assistant_response(messages)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_assistant_response(self, messages: List[Dict[str, str]]) -> Union[str, Dict]:
        """
        Sends messages to the OpenAI API and retrieves the response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            Union[str, Dict]: The response from the OpenAI API.
        """
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                **self.chat_config.to_dict()
            )
            finish_reason = response['choices'][0]['finish_reason']
            if finish_reason == 'stop':
                return response['choices'][0]['message']['content']
            elif finish_reason == 'length':
                return "Error: Incomplete response due to token limit"
            elif finish_reason == 'function_call':
                return "Error: Function call detected"
            elif finish_reason == 'content_filter':
                return "Error: Content filtered"
            else:
                return "Error: Unknown response finish reason"
        except Exception as e:
            return f"Error: {str(e)}"

# # Use the loaded configuration from openai_llm
# chat_bot = OpenAIChatBot(model="gpt-3.5-turbo", api_key="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", chat_config=LLMChatGPTConfig)
