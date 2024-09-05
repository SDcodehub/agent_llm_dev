from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import List, Dict, Union, Optional
import sys
import os
import tiktoken  # Import tiktoken for token counting

# Get the absolute path to the project's root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

class NVIDIAChatBot:
    # TODO change this to the config and read from there
    num_max_token_map = {
        "mistralai/mixtral-8x22b-instruct-v0.1": 32768,
        "meta/llama3-70b-instruct": 8000,  # Adjust the token limit as per your model
    }

    def __init__(self, model: str, api_key: str = None, chat_config: Optional[Dict] = None):
        """
        Initialize the NVIDIAChatBot instance.

        Args:
            model (str): The name of the Mistral model to use.
            api_key (str, optional): Your NVIDIA API key for authentication.
            chat_config (Dict, optional): Configuration for the chat bot.

        Attributes:
            model (str): The name of the Mistral model.
            api_key (str): Your NVIDIA API key.
            chat_config (Dict): Configuration for the chat bot.
            token_counter (int): Token counter for tracking token usage.

        """
        self.model = model
        self.api_key = api_key
        self.chat_config = chat_config
        self.llm = ChatNVIDIA(model=self.model, api_key=self.api_key)

    def send_messages_and_get_response(self, messages: List[Dict[str, str]]) -> Union[str, Dict]:
        """
        Sends a list of messages to the NVIDIA AI Endpoints and returns the response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            Union[str, Dict]: The response from the NVIDIA AI Endpoints.
        """
        try:
            # # Calculate the token count
            # num_tokens = self._calculate_token_count(messages)

            # # Check if the messages fit within the allowed context length
            # max_tokens = self._get_max_token_length()
            # if not self._check_message_length(num_tokens, max_tokens):
            #     raise ValueError(f"Error: Messages exceed the allowed context length for model '{self.model}'. "
            #                      f"Allowed: {max_tokens} tokens, Present: {num_tokens} tokens.")

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
            # TODO replace with the model name
            # model_name = self.model
            model_name = "gpt-4"
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

    def _get_assistant_response(self, messages: List[Dict[str, str]]) -> Union[str, Dict]:
        """
        Sends messages to the NVIDIA AI Endpoints and retrieves the response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries with 'role' and 'content' keys.

        Returns:
            Union[str, Dict]: The response from the NVIDIA AI Endpoints.
        """
        try:
            # Combine messages into a single string
            message_text = " ".join([message['content'] for message in messages])


            # Invoke the NVIDIA AI Endpoints
            response = self.llm.invoke(message_text)

            return response.content
        except Exception as e:
            return f"Error: {str(e)}"
