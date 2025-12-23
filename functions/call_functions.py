from google.genai import types

from config import WORKING_DIR

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ],
)

functions_dict = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'run_python_file': run_python_file,
    'write_file': write_file,
}

def call_function(function_call, verbose=False):
    if verbose is True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    if function_call.name not in functions_dict:
        response = {"error": f"Unknown function: {function_call.name}"}
    else:
        function = functions_dict[function_call.name](working_directory=WORKING_DIR, **function_call.args)
        response = {"result": function}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response= response
            )
        ],
    )

        
