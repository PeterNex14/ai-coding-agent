from config import WORKING_DIRECTORY
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from google.genai import types

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)

FUNCTIONS = {
    schema_get_files_info.name: get_files_info,
    schema_get_file_content.name: get_file_content,
    schema_write_file.name: write_file,
    schema_run_python_file.name: run_python_file,
}

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name
    kwargs = dict(function_call.args)

    kwargs["working_directory"] = WORKING_DIRECTORY
    function_to_call = FUNCTIONS[function_name]
    result = function_to_call(**kwargs)

    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )


