import os

from google.genai import types
from config import MAX_CHARACTERS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content from a specific file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        return _get_file_content(working_directory, file_path, MAX_CHARACTERS)
    except Exception as message:
        return f"Error: getting file content: {message}"

def _get_file_content(working_directory, file_path, max_characters):
    working_directory_abs = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))

    in_valid_target_file = os.path.commonpath([working_directory_abs, target_file]) != working_directory_abs

    if in_valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file, "r") as f:
        file_content_stirng = f.read(max_characters)


        if f.read(1):
            file_content_stirng += f'[...File "{file_path}" truncated at {max_characters} max_characters]'

        return file_content_stirng


