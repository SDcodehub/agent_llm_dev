from llms.openai_llm import ChatGPTConfig
from typing import List, Dict, Union, Optional
import sys
import os
import openai
import tiktoken  # Import tiktoken for token counting

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

# Get the absolute path to the project's root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)




class OpenAIChatBot:
    num_max_token_map = {
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
        "gpt-3.5-turbo-0613": 4096,
        "gpt-3.5-turbo-16k-0613": 16384,
        "gpt-4": 8192,
        "gpt-4-0613": 8192,
        "gpt-4-32k": 32768,
    }

    def __init__(self, model: str, api_key: str = None, chat_config: Optional[ChatGPTConfig] = None):
        """
        Initialize the OpenAIChatBot instance.

        Args:
            model (str): The name of the GPT-3.5 model to use.
            api_key (str, optional): Your OpenAI API key for authentication.
            chat_config (ChatGPTConfig, optional): Configuration for the chat bot.

        Attributes:
            model (str): The name of the GPT-3.5 model.
            api_key (str): Your OpenAI API key.
            chat_config (ChatGPTConfig): Configuration for the chat bot.
            token_counter (int): Token counter for tracking token usage.

        """
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
            # Calculate the token count
            num_tokens = self._calculate_token_count(messages)

            # Check if the messages fit within the allowed context length
            max_tokens = self._get_max_token_length()
            if not self._check_message_length(num_tokens, max_tokens):
                raise ValueError(f"Error: Messages exceed the allowed context length for model '{self.model}'. "
                                 f"Allowed: {max_tokens} tokens, Present: {num_tokens} tokens.")

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
            if model_name in self.num_max_token_map:
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
            else:
                raise ValueError(f"Model '{model_name}' is not supported.")
        except KeyError:
            raise ValueError(f"Model '{model_name}' is not supported for token counting.")
        except Exception as e:
            raise ValueError(f"Error calculating token count: {str(e)}")


    def _check_message_length(self, num_tokens: int, max_tokens: int) -> bool:
        """
        Checks if the provided number of tokens fit within the allowed context length for the model.

        Args:
            num_tokens (int): The number of tokens used by the messages.
            max_tokens (int): The maximum allowed token length for the model.

        Returns:
            bool: True if the messages fit within the allowed context length, False otherwise.
        """
        return num_tokens <= max_tokens

    def _get_max_token_length(self) -> int:
        """
        Gets the maximum allowed token length for the model.

        Returns:
            int: The maximum allowed token length.
        """
        try:
            model_name = self.model
            if model_name in self.num_max_token_map:
                return self.num_max_token_map[model_name]
            else:
                raise ValueError(f"Model '{model_name}' is not supported.")
        except KeyError:
            raise ValueError(f"Model '{model_name}' is not supported for token counting.")
        except Exception as e:
            raise ValueError(f"Error getting maximum token length: {str(e)}")

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))  # Apply the decorator here
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