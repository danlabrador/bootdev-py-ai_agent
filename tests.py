from functions.get_files_info import get_files_info


def print_results(results, directory):
    if directory == ".":
        directory = "current"
    print(f"Result for {directory} directory:\n{results}")


print_results(get_files_info("calculator", "."), ".")
print_results(get_files_info("calculator", "pkg"), "pkg")
print_results(get_files_info("calculator", "/bin"), "/bin")
print_results(get_files_info("calculator", "../"), "../")
