import os
from functions.validation import *
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = f'{content[:MAX_CHARS]}[...File truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the first {MAX_CHARS} characters of a specified file in the the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
