import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
        list_path = []

        if not valid_target_dir:
            return f"Cannot list '{directory}' as it is outside the permitted working directory"

        if not os.path.isdir(target_dir):
            return f"'{directory}' is not a directory"

        
        for items in os.listdir(target_dir):
            list_path.append(f"  - {items}: file_size={os.path.getsize(os.path.join(target_dir, items))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, items))}")

        return "\n".join(list_path)
    except Exception as e:
        return f"Error listing files: {e}"

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