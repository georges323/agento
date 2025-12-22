import os

def get_files_info(working_directory, directory="."):
    print(f"Result for {'current' if directory == '.' else f"'{directory}'"} directory:")

    try:
        __handle_get_files_info(working_directory, directory)
    except Exception as message:
        print(f"  Error: {message}")

# added a working directory here to limit what the LLM sees
def __handle_get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))

    # Checks if the constructed target_dir shares a commonpath to avoid problems
    valid_targer_dir = os.path.commonpath([working_directory_abs, target_dir]) != working_directory_abs

    if valid_targer_dir:
        raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

    if not os.path.isdir(target_dir):
        raise Exception(f'"{directory}" is not a directory')

    names_list = os.listdir(target_dir)

    for name in names_list:
        __output_path_meta_data(target_dir, name)


def __output_path_meta_data(directory, name):
    path = os.path.join(directory, name)

    print(f'  - {name}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path):
}')
    
    





