import os

class CodeFileGenerator:
    def __init__(self, filename, extension, language, docstring, code, file_path):
        self.filename = filename
        self.extension = extension
        self.language = language
        self.docstring = docstring
        self.code = code
        self.file_path = file_path

    def create_repository(self):
        for file_info in self.file_info_list:
            self.create_code_file(file_info)

    def create_code_file(self):
        # Create the file with the specified filename and extension
        file_name_with_extension = f"{self.filename}.{self.extension}"
        file_full_path = os.path.join(self.file_path, file_name_with_extension)

        if not os.path.exists(file_full_path):
            with open(file_full_path, 'w') as code_file:
                # Add the docstring to the file
                code_file.write(f'\'\'\'{self.language}\n')
                code_file.write(f'{self.docstring}\n')
                code_file.write('\'\'\'\n\n')

                # Add the code to the file
                code_file.write(self.code)

        print(f"File '{file_name_with_extension}' created at '{file_full_path}'.")


if __name__ =='__main__':
    # Example usage:
    file_info = ("time_checking_app", "py", "Python", "This is a sample Python code file.", "print('Hello, World!')")
    file_path = "/path/to/your/directory"

    generator = CodeFileGenerator(file_info, file_path)
    generator.create_code_file()
