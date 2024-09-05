import re


class TaskParser:
    def __init__(self, task_name, response):
        self.task_name = task_name
        self.response = response

    def parse_info(self):
        if self.response.startswith("<INFO> "):
            return self.response.split("<INFO> ")[-1].strip()

    def extract_code_block(self):
        # Define a regular expression pattern to match the code block format
        pattern = r'^(.*)\n```(\w+)\n(\'\'\'\n.*\n\'\'\'\n)([^`]+)```'
        # print(self.response)
        # Search for matches in the input text
        match = re.search(pattern, self.response, re.MULTILINE | re.DOTALL)

        if match:
            # Extract the matched components
            code_block_header = match.group(1).strip()
            filename_match = re.search(r'([^\s]+)\.(\w+)', code_block_header)

            if filename_match:
                filename = filename_match.group(1)
                extension = filename_match.group(2)
            else:
                filename = code_block_header
                extension = None

            language = match.group(2).strip()
            docstring = match.group(3).strip("'''\n")
            code = match.group(4).strip()

            return filename, extension, language, docstring, code

        return None  # Return None if no match is found


    def extract_image_info(self):
        # Define a regular expression pattern to match the desired format
        pattern = r'^(.*?):\s(.*?)$'

        # Use re.match to find the first match in the input string
        match = re.match(pattern, self.response)

        if match:
            # Extract the image name and description from the matched groups
            image_name = match.group(1)
            description = match.group(2)
            return image_name, description
        else:
            # Return None if there is no match
            return None, None

    def parse_output(self):
        if self.task_name in ["DemandAnalysis", "LanguageChoose"]:
            return self.parse_info()
        elif self.task_name in ["ArtDesign"]:
            # "button_1.png: The button with the number \"1\" on it.",
            # "button_multiply.png: The button with the multiplication symbol (\"*\") on it.
            return self.extract_image_info()
        elif self.task_name in ["Coding", "ArtIntegration"]:
            return self.extract_code_block()
        elif self.task_name in ["CodeComplete", "CodeReviewComment",
                                "CodeReviewModification", "test_reports",
                                "TestErrorSummary", "TestModification",
                                "EnvironmentDoc"]:
            # TODO implement logif for this processing
            # "button_1.png: The button with the number \"1\" on it.",
            # "button_multiply.png: The button with the multiplication symbol (\"*\") on it.
            return None
        else:
            return None


if __name__ == "__main__":
    # Example usage:
    task_name = "DemandAnalysis"
    response = "<INFO> PowerPoint"

    parser = TaskParser(task_name, response)
    parsed_output = parser.parse_output()
    print(parsed_output)
    print("-" * 10)

    # Example usage:
    task_name = "Coding"
    response = """time_checking_app.py
```python
'''
Time Checking App

This app allows users to check the current time in different time zones.

Usage:
    python time_checking_app.py

Author:
    Your Name
'''
from datetime import datetime
from time_zones import TimeZones    
if __name__ == "__main__":
    main()
    ```"""

    parser = TaskParser(task_name, response)
    parsed_output = parser.parse_output()
    print(parser.parse_output())
    if parsed_output:
        filename, extension, language, docstring, code = parsed_output
        print("Filename:", filename)
        print("-"*10)
        print("Extension:", extension)
        print("-" * 10)
        print("Language:", language)
        print("-" * 10)
        print("Docstring:", docstring)
        print("-" * 10)
        print("Code:", code)
    else:
        print("Code block not found in the input text.")
