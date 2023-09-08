import os
import sys

root = os.path.dirname(__file__)
sys.path.append(root)

from llms.openai_llm import ChatGPTConfig

config = ChatGPTConfig(
)

print(config)

config.save_to_file("my_config.json")

loaded_config = ChatGPTConfig.load_from_file("my_config.json")
print(loaded_config)



