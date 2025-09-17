import os


def get_files_info(working_directory, directory="."):
    try:
        current_working_directory_path = os.getcwd()
        working_directory_path = working_directory

        if working_directory not in current_working_directory_path:
            working_directory_path = os.path.abspath(
                os.path.join(current_working_directory_path, working_directory_path)
            )

        directory_path = os.path.abspath(
            os.path.join(working_directory_path, directory)
        )

        if not directory_path.startswith(working_directory_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'

        objects_rel_path_list = os.listdir(directory_path)
        objects_metadata_list = []

        for obj in objects_rel_path_list:
            raw_obj_full_path = os.path.join(directory_path, obj)
            obj_full_path = os.path.abspath(raw_obj_full_path)
            obj_file_size = f"file_size={os.path.getsize(obj_full_path)} bytes"
            is_obj_dir_str = f"is_dir={os.path.isdir(obj_full_path)}"
            obj_metadata = f"- {obj}: {obj_file_size}, {is_obj_dir_str}"
            objects_metadata_list.append(obj_metadata)

        objects_metadata = "\n".join(objects_metadata_list)
        return objects_metadata
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    results = get_files_info(os.getcwd(), "sample")
    print(results)
