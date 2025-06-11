import os
from functions.validation import *
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        directory = os.path.dirname(target_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        print("\n", f"Attempting to write to file '{file_path}':\n\n{content}\n")
        if input("Confirm write. Enter 'yes' to confirm:") != "yes":
            raise Exception("User interrupted write")

        with open(target_file, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory. Any directories or files in the file path that do not exist yet, are created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The new content to write to the specified file. The file's old content will be overriden.",
            ),
        },
        required=["file_path", "content"],
    ),
)
