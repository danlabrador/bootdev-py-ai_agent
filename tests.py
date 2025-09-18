from functions.get_files_content import get_files_content
from functions.get_files_info import get_files_info


def print_dir_results(results, directory):
    if directory == ".":
        directory = "current"
    print(f"Result for {directory} directory:\n{results}")


def print_file_results(results, file):
    print(
        f"\n\nResult for {file} directory:\n--------------------------------------------\n{results}\n--------------------------------------------"
    )


# print_results(get_files_info("calculator", "."), ".")
# print_results(get_files_info("calculator", "pkg"), "pkg")
# print_results(get_files_info("calculator", "/bin"), "/bin")
# print_results(get_files_info("calculator", "../"), "../")
print_file_results(get_files_content("calculator", "main.py"), "main.py")
print_file_results(
    get_files_content("calculator", "pkg/calculator.py"), "pkg/calculator.py"
)
print_file_results(get_files_content("calculator", "/bin/cat"), "/bin/cat")
print_file_results(
    get_files_content("calculator", "pkg/does_not_exist"), "pkg/does_not_exist.py"
)
