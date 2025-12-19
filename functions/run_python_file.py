import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))

    try:
        if os.path.commonpath([absolute_path, target_file]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(target_file) or not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]

        if args != None:
            command.extend(args)
        
        result = subprocess.run(
            command,
            cwd=absolute_path,
            text=True,
            capture_output=True,
            timeout=30,
        )
        output = []
        
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")

        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")

        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file relative to the working directory",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Items of the arguments to pass to the Python file"
                ),
                description="Arguments to pass to the Python file"
            )
        }
    )
)