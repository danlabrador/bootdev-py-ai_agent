import os
import subprocess


def run_python_file(working_directory, raw_file_path, args=[]):
    try:
        current_working_directory_path = os.getcwd()
        working_directory_path = working_directory

        if working_directory not in current_working_directory_path:
            working_directory_path = os.path.abspath(
                os.path.join(current_working_directory_path, working_directory_path)
            )

        file_path = os.path.abspath(os.path.join(working_directory_path, raw_file_path))

        # If the file_path is outside the working directory, return error string
        if not file_path.startswith(working_directory_path):
            return f'Error: Cannot execute "{raw_file_path}" as it is outside the permitted working directory'

        # If the file_path doesn't exist, return error string
        if not os.path.isfile(file_path):
            return f'Error: File "{raw_file_path}" not found.'

        # If the file doesn't end with ".py", return error string
        if not raw_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        output = subprocess.run(
            ["python", file_path] + args, capture_output=True, text=True, timeout=30
        )

        return_code = output.returncode
        if return_code != 0:
            return f"Process exited with code {return_code}"

        output_list = []

        text_output = output.stdout.strip()
        text_error = output.stderr.strip()

        if len(text_output) > 0:
            output_list.append("STDOUT: " + text_output)

        if len(text_error) > 0:
            output_list.append("STDERR: " + text_error)

        if len(output_list) == 0:
            return f"No output produced"

        return "\n".join(output_list)

    except Exception as e:
        return f"Error: executing Python file: {e}"
