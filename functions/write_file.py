from ntpath import isdir
import os

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
