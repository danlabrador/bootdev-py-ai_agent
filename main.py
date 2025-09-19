# cspell: ignore dotenv genai bootdev
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)


def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)

    command_args = sys.argv[1:]
    command_flags = list(filter(lambda x: x.startswith("--"), command_args))
    command_prompt_list = list(filter(lambda x: not x.startswith("--"), command_args))
    command_prompt = command_prompt_list[0]

    is_verbose = "--verbose" in command_flags

    if len(command_prompt_list) != 1:
        sys.exit(
            'Please include prompt in your command enclosed in parenthesis: uv run main.py "your prompt here"'
        )

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    model_name = "gemini-2.0-flash-001"
    messages = [command_prompt]

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    response_text = response.text
    response_usage = response.usage_metadata
    function_calls = (
        response.function_calls if response.function_calls is not None else []
    )

    # Print outputs
    if response_text is not None:
        print(response_text)

    for function_call in function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")

    if is_verbose:
        print(f"User prompt: {command_prompt}")
        print(f"Prompt tokens: {response_usage.prompt_token_count}")  # type: ignore
        print(f"Response tokens: {response_usage.candidates_token_count}")  # type: ignore


if __name__ == "__main__":
    main()
