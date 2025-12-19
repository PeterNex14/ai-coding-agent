# AI Agent Boot

This repository contains a Python-based AI Agent built as part of the **"Build an AI Agent with Python"** guided project on [Boot.dev](https://boot.dev).

## 🤖 What is this?

This project is a CLI-based AI coding assistant (Agent) capable of performing autonomous tasks on the local file system. It leverages the **Google Gemini API** to understand user prompts and executes actions using a set of defined tools (Function Calling).

The agent can:
- **Explore** the file system (list files and directories).
- **Read** file contents.
- **Write** code and create files.
- **Execute** Python scripts directly.

## 🛠️ What I've Done

In this project, I have built an agentic workflow including:
- **Tool Implementation**: Created modular Python functions (`get_files_info`, `get_file_content`, `write_file`, `run_python_file`) that the AI can invoke.
- **Gemini Integration**: Configured the Google GenAI SDK to communicate with the Gemini 2.0 Flash model.
- **Function Calling System**: Built a mechanism to parse the AI's tool call requests, execute the corresponding Python functions, and feed the results back to the model.
- **REPL Loop**: Implemented a robust "Read-Eval-Print Loop" inside `main.py` that allows for multi-turn reasoning (the agent can call a tool, see the result, and decide the next step).
- **Security & Safety**: Added safeguards like restricting file access to a specific `WORKING_DIRECTORY` to prevent the agent from modifying system files outside the sandbox.

## 🧠 What I've Learned

Building this agent taught me several core concepts of Agentic AI:
- **LLM as a Controller**: How to make a Large Language Model "act" rather than just "chat" by giving it tools.
- **The ReAct Pattern**: Understanding the reasoning loop (Thought -> Action -> Observation -> Response).
- **Function Calling Schemas**: How to define JSON schemas for tools so the LLM understands exactly how to call them.
- **State Management**: Managing the conversation history (`messages` list) to maintain context across multiple tool executions.

## 🚀 How to Run

1.  Clone the repository.
2.  Install dependencies (using `uv` or `pip`):
    ```bash
    uv sync
    # or
    pip install -r requirements.txt
    ```
3.  Set your `GEMINI_API_KEY` in a `.env` file.
4.  Run the agent:
    ```bash
    python main.py "your instruction here"
    ```
