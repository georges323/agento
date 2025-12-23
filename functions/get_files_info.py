import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        return _handle_get_files_info(working_directory, directory)
    except Exception as message:
        return f"Error listing files: {message}"

# added a working directory here to limit what the LLM sees
def _handle_get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))

    # Checks if the constructed target_dir shares a commonpath to avoid problems
    invalid_targer_dir = os.path.commonpath([working_directory_abs, target_dir]) != working_directory_abs

    if invalid_targer_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    files_info = []

    for name in os.listdir(target_dir):
        path = os.path.join(target_dir, name)

        file_info = f'- {name}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path):}'

        files_info.append(file_info)

    return "\n".join(files_info)







