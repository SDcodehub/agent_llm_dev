import os
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, Sequence, Union

# Define the path to the 'configs' directory within your package
CONFIGS_DIR = os.path.join(os.path.dirname(__file__), "../configs")


@dataclass(frozen=True)
class ChatGPTConfig:
    """
    Defines the parameters for generating chat completions using the OpenAI API.
    """

    temperature: float = 0.2
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: Optional[Union[str, Sequence[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    logit_bias: Dict = field(default_factory=dict)
    user: str = ""

    def __str__(self):
        return (
            f"ChatGPTConfig("
            f"temperature={self.temperature}, "
            f"top_p={self.top_p}, "
            f"n={self.n}, "
            f"stream={self.stream}, "
            f"stop={self.stop}, "
            f"max_tokens={self.max_tokens}, "
            f"presence_penalty={self.presence_penalty}, "
            f"frequency_penalty={self.frequency_penalty}, "
            f"logit_bias={self.logit_bias}, "
            f"user='{self.user}'"
            f")"
        )

    def to_dict(self):
        """
        Convert the configuration to a dictionary.
        """
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": self.stop,
            "max_tokens": self.max_tokens,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "logit_bias": self.logit_bias,
            "user": self.user,
        }

    def save_to_file(self, filename):
        """
        Save the configuration to a JSON file in the 'configs' directory.
        """
        config_dict = self.to_dict()
        config_path = os.path.join(CONFIGS_DIR, filename)
        with open(config_path, "w") as config_file:
            json.dump(config_dict, config_file)

    @classmethod
    def load_from_file(cls, filename):
        """
        Load a configuration from a JSON file in the 'configs' directory.
        """
        config_path = os.path.join(CONFIGS_DIR, filename)
        with open(config_path, "r") as config_file:
            config_dict = json.load(config_file)
        return cls(**config_dict)
    

if __name__ == '__main__':

    import os
    import sys

    root = os.path.dirname(__file__)
    sys.path.append(root)

    from llms.openai_llm import ChatGPTConfig

    config = ChatGPTConfig(
    )

    print(config)

    config.save_to_file("llmconfig.json")

    loaded_config = ChatGPTConfig.load_from_file("llmconfig.json")
    print(loaded_config)
