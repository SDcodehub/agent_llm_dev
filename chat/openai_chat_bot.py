from llms.openai_llm import ChatGPTConfig
from typing import List, Dict, Union, Optional
import sys
import os
import openai
import tiktoken  # Import tiktoken for token counting

# Get the absolute path to the project's root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)


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
        token_counter (int): Token counter for tracking token usage.

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
        self.token_counter = 0  # Initialize the token counter

    def send_messages_and_get_response(self, messages: List[Dict[str, str]]) -> Union[str, Dict]:
        """
        Sends a list of messages to the OpenAI API and returns the response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            Union[str, Dict]: The response from the OpenAI API.
        """
        try:
            # Calculate and update the token count for the current messages
            num_tokens = self._calculate_token_count(messages)
            self.token_counter += num_tokens  # Update the token counter
            response = self._get_assistant_response(messages)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def _calculate_token_count(self, messages: List[Dict[str, str]]) -> int:
        """
        Calculates the number of tokens used by a list of messages.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            int: The number of tokens used.
        """
        try:
            model_name = self.model
            encoding = tiktoken.encoding_for_model(model_name)
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":
                        num_tokens += -1  # Role is always required and always 1 token
            num_tokens += 2  # Every reply is primed with <im_start>assistant
            return num_tokens
        except KeyError:
            raise ValueError(f"Model '{model_name}' is not supported for token counting.")
        except Exception as e:
            raise ValueError(f"Error calculating token count: {str(e)}")

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
