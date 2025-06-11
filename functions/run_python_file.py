import os
from functions.validation import *
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path_to_working_directory = os.path.abspath(working_directory)
        target_file = get_absolute_target_path(absolute_path_to_working_directory, file_path)

        if not target_is_in_working_directory(absolute_path_to_working_directory, target_file):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python File.'

        commands = ["python", target_file]
        if args:
            commands.extend(args)

        result = subprocess.run(
            args=commands,
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

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file within the working directory and returns the output from the interpretr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass the the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass the the Python file.",
                ),
            ),
        },
        required=["file_path"]
    ),
)
