import os
import getpass


def check_api_key(api_key_var_name: str = 'OPENAI_API_KEY') -> str:
    """
    Check if an API key is available in the environment variable or prompt the user to enter it.

    Args:
        api_key_var_name (str): The name of the API key environment variable.

    Returns:
        str: The API key.
    """
    # Check if the API key environment variable is set
    api_key = os.environ.get(api_key_var_name)

    if api_key is None:
        # If not set, prompt the user to enter the API key
        api_key = getpass.getpass(prompt=f"Enter your {api_key_var_name} API key (secret): ")

        # Optionally, you can save it to the environment variable
        os.environ[api_key_var_name] = api_key

    return api_key
