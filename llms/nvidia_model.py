from enum import Enum

class NvidiaModelType(Enum):
    """
    Enumeration of Nvidia model types with their corresponding actual names.

    Attributes:
        llama3-70b-instruct (str): The actual name for Model A.
        MODEL_B (str): The actual name for Model B.
        MODEL_C (str): The actual name for Model C.
        STUB (str): A stub model, for example purposes.
    """
    LLAMA3_70B_INSTRUCT: str = "meta/llama3-70b-instruct"
    MODEL_B: str = "nvidia-model-b"
    MODEL_C: str = "nvidia-model-c"
    STUB: str = "nvidia-stub"

def nvidia_model_type(arg):
    try:
        return NvidiaModelType[arg]
    except KeyError:
        raise ValueError(f"Invalid Nvidia model type: {arg}")
