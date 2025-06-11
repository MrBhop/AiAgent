import os
from functions.validation import *
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_directory = get_absolute_target_path(absolute_path_to_working_directory, directory)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_directory):
            return f'Error: Cannot list "{directory}" as it is outside the premitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        output = []
        for item in os.listdir(target_directory):
            path = os.path.join(target_directory, item)
            output.append(f' - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}')

        return '\n'.join(output)

    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
