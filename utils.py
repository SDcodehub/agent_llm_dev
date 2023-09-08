import os

def generate_folder_structure(directory, indent=""):
    """
    Generate a text-based representation of the folder structure, including folders, subfolders, and files (excluding hidden folders).

    Args:
        directory (str): The directory for which to generate the structure.
        indent (str): The current level of indentation for formatting.

    Returns:
        str: A text-based representation of the folder structure.
    """
    folder_structure = ""
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.name.startswith("."):
                    folder_structure += f"{indent}+-- {entry.name}/\n"
                    folder_structure += generate_folder_structure(
                        os.path.join(directory, entry.name),
                        indent + "|   "
                    )
                elif entry.is_file() and not entry.name.startswith("."):
                    folder_structure += f"{indent}    {entry.name}\n"
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return folder_structure

if __name__ == "__main__":
    directory = input("Enter the path to the directory: ")

    if os.path.exists(directory):
        folder_structure = generate_folder_structure(directory)
        print(f"Folder structure for '{directory}':\n")
        print(folder_structure)
    else:
        print("The specified directory does not exist.")
