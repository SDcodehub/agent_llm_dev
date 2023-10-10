import os

def get_config_paths() -> tuple:
    """
    Get the paths to configuration files.

    Returns:
        tuple: A tuple of paths to configuration files.
    """
    # Get the absolute path to the directory where your config_utils.py script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one level to the parent directory to remove "utils" from the path
    parent_dir = os.path.dirname(script_dir)

    # Specify the directory where your config files are located (relative to the parent directory)
    config_dir = os.path.join(parent_dir, "configs")

    # Define the names of the config files
    agents_config_file = "AgentsConfig.json"
    llm_config_file = "my_config.json"
    taskchain_config_file = "TaskchainConfigs.json"
    task_config_file = "TaskConfig.json"

    # Construct the full paths to the config files
    agents_config_path = os.path.join(config_dir, agents_config_file)
    llm_config_path = os.path.join(config_dir, llm_config_file)
    taskchain_config_path = os.path.join(config_dir, taskchain_config_file)
    task_config_path = os.path.join(config_dir, task_config_file)

    return agents_config_path, llm_config_path, taskchain_config_path, task_config_path
