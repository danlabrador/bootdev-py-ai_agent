# cspell: ignore genai

from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_call_part.args
    if function_name is None or function_args is None:
        result = (
            "Either name or args is not provided.\n"
            + f"  function_call_part.name: {function_name}\n"
            + f"  function_call_part.args: {function_args}\n"
        )
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name="None",
                    response={"error": result},
                )
            ],
        )

    result = None

    match function_call_part.name:
        case "get_files_info":
            result = get_files_info("./calculator", **function_args) + "\n"
        case "get_file_content":
            result = get_file_content("./calculator", **function_args) + "\n"
        case "write_file":
            result = write_file("./calculator", **function_args) + "\n"
        case "run_python_file":
            result = run_python_file("./calculator", **function_args) + "\n"
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
