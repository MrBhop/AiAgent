import os
from functions.validation import *

__MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot read "{file_path}" as it is outside the premitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as f:
            content = f.read(__MAX_CHARS + 1)
            if len(content) > __MAX_CHARS:
                content = f'{content[:__MAX_CHARS]}[...File truncated at {__MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f'Error: {e}'
