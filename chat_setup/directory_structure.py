import os
from datetime import datetime

class DirectoryStructure:
    def __init__(self, app_name: str):
        """
        Initialize a DirectoryStructure object.

        Args:
            app_name (str): The name of the application.
        """
        self.app_name = app_name
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.base_dir: str = self.get_base_directory()
        self.logs_dir: str = self.get_logs_directory()
        self.codes_dir: str = self.get_codes_directory()
        self.configs_dir: str = self.get_configs_directory()
        self.chat_history_dir: str = self.get_chat_history_directory()

    def get_base_directory(self) -> str:
        """
        Get the base directory path.

        Returns:
            str: The base directory path.
        """
        return f"outputs/{self.app_name}_{self.timestamp}"

    def _create_directory(self, directory: str) -> None:
        """
        Create a directory if it doesn't exist.

        Args:
            directory (str): The directory path to create.
        """
        os.makedirs(directory, exist_ok=True)

    def create_structure(self) -> None:
        """
        Create the directory structure for the application.
        """
        self._create_directory(self.base_dir)
        self._create_directory(self.logs_dir)
        self._create_directory(self.codes_dir)
        self._create_directory(self.configs_dir)
        self._create_directory(self.chat_history_dir)

    def get_logs_directory(self) -> str:
        """
        Get the logs directory path.

        Returns:
            str: The logs directory path.
        """
        return os.path.join(self.base_dir, "logs")

    def get_codes_directory(self) -> str:
        """
        Get the codes directory path.

        Returns:
            str: The codes directory path.
        """
        return os.path.join(self.base_dir, "codes")

    def get_configs_directory(self) -> str:
        """
        Get the configs directory path.

        Returns:
            str: The configs directory path.
        """
        return os.path.join(self.base_dir, "configs")

    def get_chat_history_directory(self) -> str:
        """
        Get the chat history directory path.

        Returns:
            str: The chat history directory path.
        """
        return os.path.join(self.base_dir, "chat_history")
