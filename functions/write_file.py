import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contnent to a file from a specific file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of where the content will be wriiten to relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written into the file given by the file path.",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        return _handle_write_file(working_directory, file_path, content)
    except Exception as message:
        return f"Error: {message}"

def _handle_write_file(working_directory, file_path, content):
    working_directory_abs = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    invalid_target_file = os.path.commonpath([working_directory_abs, target_file]) != working_directory_abs

    if invalid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    parent_dirs = os.path.dirname(target_file)
    os.makedirs(parent_dirs, exist_ok=True)
    
    with open(target_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
