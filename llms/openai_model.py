from enum import Enum


class ModelType(Enum):
    """
    Enumeration of model types with their corresponding actual names.

    Attributes:
        GPT_3_5_TURBO (str): The actual name for the GPT-3.5 Turbo model.
        GPT_4 (str): The actual name for the GPT-4 model.
        GPT_4_32K (str): The actual name for the GPT-4 32K model.
        STUB (str): A stub model, for example purposes.
    """
    GPT_3_5_TURBO: str = "gpt-3.5-turbo-16k-0613"
    GPT_4: str = "gpt-4"
    GPT_4_32K: str = "gpt-4-32k"


def model_type(arg):
    try:
        return ModelType[arg]
    except KeyError:
        raise ValueError(f"Invalid model type: {arg}")
