import os
from functions.validation import *
import subprocess

def run_python_file(working_directory, file_path):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python File.'

        result = subprocess.run(
            args=["python", target_file],
            timeout=30,
            capture_output=True,
            cwd=absolute_path_to_working_directory,
            text=True
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')

        if len(output) == 0:
            return "No output produced."
        return "\n".join(output)

    except Exception as e:
        return f'Error: {e}'
