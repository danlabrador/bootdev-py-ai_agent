# AI Agent with Google Gemini

A Python-based AI agent that interacts with files in a sandboxed environment using Google's Gemini API. This project is based on a Boot.dev guided project, enhanced with proper type definitions from the genai documentation for more consistent and reliable results.

## Features

- File system operations (read, write, list files)
- Python script execution with arguments
- Sandboxed environment for security
- Iterative processing with function calling
- Mathematical expression evaluation via calculator module
- Verbose mode for detailed operation tracking

## Prerequisites

- Python 3.13+
- Google Gemini API key
- uv package manager

## Installation

1. Clone the repository:

```bash
git clone https://github.com/danlabrador/bootdev-py-ai_agent.git
cd bootdev-py-ai_agent
```

2. Install dependencies:

```bash
uv sync
```

3. Set up environment variables:

```bash
cp .env.example .env
# Add your GEMINI_API_KEY to the .env file
```

## Usage

### Running the AI Agent

```bash
# Basic usage
uv run main.py "your prompt here"

# Verbose mode for detailed output
uv run main.py "your prompt here" --verbose
```

### Examples

```bash
# List all files in the calculator directory
uv run main.py "list all files in the calculator directory"

# Run calculator tests
uv run main.py "run the calculator tests"

# Evaluate a mathematical expression
uv run main.py "use the calculator module we have to calculate 3 * 4 + 5
```

## Project Structure

```
.
|-- main.py                 # Main agent loop implementation
|-- calculator/             # Example calculator application
|   |-- main.py
|   |-- tests.py
|   |-- pkg/
|       |-- calculator.py  # Calculator class with expression evaluation
|       |-- render.py
|-- functions/              # Agent function implementations
    |-- call_function.py   # Function dispatcher
    |-- get_file_content.py
    |-- get_files_info.py
    |-- run_python_file.py
    |-- write_file.py
```

## Security

The agent implements several security measures:

- All file operations are restricted to relative paths within the working directory
- Path traversal attempts are blocked
- Maximum of 20 iterations per agent session to prevent infinite loops
- Sandboxed execution environment

## Configuration

The agent uses the following configuration:

- Model: `gemini-2.0-flash-001`
- Maximum iterations: 20
- Available functions: file operations (read, write, list) and Python execution

## Author

**Dan Labrador**
Email: github.community@danlabrador.com
GitHub: [@danlabrador](https://github.com/danlabrador)

## Acknowledgments

- This project is based on a guided project from [Boot.dev](https://boot.dev)
- Enhanced with proper type definitions from the official Google genai documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
