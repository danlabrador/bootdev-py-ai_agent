import os


def write_file(working_directory, raw_file_path, content):
    try:
        current_working_directory_path = os.getcwd()
        working_directory_path = working_directory

        if working_directory not in current_working_directory_path:
            working_directory_path = os.path.abspath(
                os.path.join(current_working_directory_path, working_directory_path)
            )

        file_path = os.path.abspath(os.path.join(working_directory_path, raw_file_path))

        if not file_path.startswith(working_directory_path):
            return f'Error: Cannot write to "{raw_file_path}" as it is outside the permitted working directory'

        # If the directory of file doesn't exist, create it.
        new_directory = "/".join(raw_file_path.split("/")[:-1])
        new_directory_path = os.path.abspath(
            os.path.join(working_directory_path, new_directory)
        )
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)

        # Write or overwrite the file
        with open(file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{raw_file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
