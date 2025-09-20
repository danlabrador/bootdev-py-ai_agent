# cspell: ignore dotenv genai bootdev
import os
import sys
import textwrap
import traceback
import warnings

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=r"there are non-text parts in the response: \['function_call'\]",
)

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

        If not prompted with a file path, list all the files first and continue from there.

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

        If responding with text, do not use markdown formatting except when using lists. Format as plain text.
    """

    model_name = "gemini-2.0-flash-001"
    messages = [types.Content(parts=[types.Part(text=command_prompt)], role="user")]

    iterations = 0
    is_done = False

    while iterations < 20:
        try:
            # Use Gemini to generate a response
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            response_text = None
            response_usage = response.usage_metadata
            function_calls = (
                response.function_calls if response.function_calls is not None else []
            )

            # Add response contents to messages
            for candidate in response.candidates or []:
                if candidate.content is not None:
                    messages.append(candidate.content)

                if candidate.content is not None and candidate.content.parts:
                    response_text = candidate.content.parts[0].text

                    if response_text and iterations == 0:
                        print(f"{response_text.strip()}")

                    if response_text and iterations != 0:
                        print(f"\n{response_text.strip()}")

            # Break if no more function calls
            if response_text is not None and len(function_calls) == 0:
                is_done = True
                break

            # Execute function calls and add function call results to messages
            for function_call_part in function_calls:
                function_responses = call_function(
                    function_call_part, verbose=is_verbose
                )

                if function_responses.parts is None:
                    raise TypeError(
                        'Object of type "None" is not subscriptable. We expect types.Content.parts to be a list.'
                    )

                if function_responses.parts[0].function_response is None:
                    raise KeyError(
                        '"response" is not a known attribute of types.Content.parts[0].function_response="None"'
                    )

                if is_verbose:
                    print(
                        f"-> {function_responses.parts[0].function_response.response}"
                    )

                # Add response to messages
                for response in function_responses.parts:
                    if response.function_response is not None:
                        messages.append(
                            types.Content(
                                parts=[
                                    types.Part(
                                        function_response=types.FunctionResponse(
                                            name=function_call_part.name,
                                            response=response.function_response.response,
                                        )
                                    )
                                ],
                                role="user",
                            )
                        )

        except Exception:
            messages.append(
                types.Content(
                    parts=[types.Part(text=f"Error: {traceback.format_exc()}")],
                    role="user",
                )
            )

        iterations += 1

    if not is_done:
        not_done_system_prompt = """
            You are a helpful AI documentation specialist.

            Your task is to create a summary of the changes the AI agent made in the working directory.

            The AI agent can:
                - List files and directories
                - Read file contents
                - Execute Python files with optional arguments
                - Write or overwrite files

            You give a brief summary of what changes the model made in response to the users request.

            Also mention that the AI agent has reached its limit of 20 iterations.

            Do not response with function_calls. Always respond with a text.
        """

        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=not_done_system_prompt
            ),
        )

        response_text = response.text

        if response_text is not None:
            print(response_text)
        else:
            print(
                "The AI agent has reached it's limit of 20 iterations. Please check diff for the changes and prompt again."
            )

    if is_verbose:
        print(f"User prompt: {command_prompt}")
        print(f"Prompt tokens: {response_usage.prompt_token_count}")  # type: ignore
        print(f"Response tokens: {response_usage.candidates_token_count}")  # type: ignore


if __name__ == "__main__":
    main()
