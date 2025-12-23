import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        return _handle_run_python_file(working_directory, file_path, args)
    except Exception as message:
        return f"Error: executing Python file: {message}"

def _handle_run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)

    target_file_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))

    is_invalid_target_file = os.path.commonpath([working_directory_abs, target_file_abs]) != working_directory_abs

    if is_invalid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    extension = file_path.split('.')[1]

    if extension != 'py':
        return f'Error: "{file_path}" is not a Python file'

    command = ['python', target_file_abs]

    if args is not None:
        command.extend(args)

    processResult = subprocess.run(command, capture_output=True, text=True, timeout=30)

    if processResult.returncode != 0:
        return f'Process exited with code {processResult.returncode}'
    
    if processResult.stdout is None or processResult.stderr is None:
        return 'No ouput produced'

    return f'STDOUT:\n{processResult.stdout}\nSTDERR:\n{processResult.stderr}\n'


    


