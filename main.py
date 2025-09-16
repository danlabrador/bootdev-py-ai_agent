# cspell: ignore dotenv genai bootdev
import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()


def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)

    print("Hello from bootdev-py-ai-agent!")
    command_args = sys.argv[1:]
    command_flags = list(filter(lambda x: x.startswith("--"), command_args))
    command_prompt_list = list(filter(lambda x: not x.startswith("--"), command_args))
    command_prompt = command_prompt_list[0]

    is_verbose = "--verbose" in command_flags

    if len(command_prompt_list) != 1:
        sys.exit(
            'Please include prompt in your command enclosed in parenthesis: uv run main.py "your prompt here"'
        )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=command_prompt,
    )

    response_text = response.text
    response_usage = response.usage_metadata

    print(response_text)

    if is_verbose:
        print(f"User prompt: {command_prompt}")
        print(f"Prompt tokens: {response_usage.prompt_token_count}")  # type: ignore
        print(f"Response tokens: {response_usage.candidates_token_count}")  # type: ignore


if __name__ == "__main__":
    main()
