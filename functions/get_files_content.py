import os


def get_files_content(working_directory, raw_file_path):
    try:
        current_working_directory_path = os.getcwd()
        working_directory_path = working_directory

        if working_directory not in current_working_directory_path:
            working_directory_path = os.path.abspath(
                os.path.join(current_working_directory_path, working_directory_path)
            )

        file_path = os.path.abspath(os.path.join(working_directory_path, raw_file_path))

        if not file_path.startswith(working_directory_path):
            return f'Error: Cannot read "{raw_file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{raw_file_path}"'

        MAX_CHARS = 10000

        with open(file_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = (
                    file_content_string[:MAX_CHARS]
                    + f'[...File "{raw_file_path}" truncated at 10000 characters]'
                )

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
