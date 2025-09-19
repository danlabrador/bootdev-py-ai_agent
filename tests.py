from functions.get_files_content import get_files_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


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


# print_file_results(get_files_content("calculator", "main.py"), "main.py")
# print_file_results(
#     get_files_content("calculator", "pkg/calculator.py"), "pkg/calculator.py"
# )
# print_file_results(get_files_content("calculator", "/bin/cat"), "/bin/cat")
# print_file_results(
#     get_files_content("calculator", "pkg/does_not_exist"), "pkg/does_not_exist.py"
# )


# # cspell: ignore morelorem amet
# print_file_results(
#     write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), "lorem.txt"
# )
# print_file_results(
#     write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
#     "pkg/morelorem.txt",
# )
# print_file_results(
#     write_file("calculator", "/tmp/temp.txt", "this should not be allowed"),
#     "/tmp/temp.txt",
# )


print_file_results(run_python_file("calculator", "main.py"), "main.py")
print_file_results(run_python_file("calculator", "main.py", ["3 + 5"]), "main.py")
print_file_results(run_python_file("calculator", "tests.py"), "tests.py")
print_file_results(run_python_file("calculator", "../main.py"), "../main.py")
print_file_results(run_python_file("calculator", "nonexistent.py"), "nonexistent.py")
