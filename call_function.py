from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

__functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args
    if verbose:
        print(f'Calling function: {function_name}({args})')
    else:
        print(f" - Calling function: {function_name}")

    if function_name in __functions:
        result = types.Part.from_function_response(
            name=function_name,
            response={"result": __functions[function_name](working_directory="./calculator", **args)},
        )
    else:
        result = types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unkown function: {function_name}"},
        )

    return types.Content(
        role="tool",
        parts=[
            result
        ],
    )
