import os
from functions.validation import *

def write_file(working_directory, file_path, content):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        directory = os.path.dirname(target_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(target_file, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
