import json
import os
import sys

from openai import OpenAI

import tools

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
client = OpenAI()

# ==================================================
# Tool definitions
# ==================================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "list_files",
        "description": (
            "List files in the repository. "
            "Use this to understand the repository structure."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "read_file",
        "description": (
            "Read a repository file. "
            "Use this to inspect source code, configuration, "
            "or other relevant files."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "run_tests",
        "description": (
            "Run the project's automated tests using pytest."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "edit_file",
        "description": (
            "Replace the complete contents of an application "
            "source file with corrected content."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path of file to edit",
                },
                "content": {
                    "type": "string",
                    "description": "Complete new file contents",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "git_diff",
        "description": (
            "Show the current uncommitted Git changes."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },

    {
        "type": "function",
        "name": "git_status",
        "description": (
            "Show Git working tree status."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },
]

# ==================================================
# Execute tools
# ==================================================

def execute_tool(name, arguments):
    if name == "list_files":
        return tools.list_files()

    if name == "read_file":
        return tools.read_file(
            arguments["path"]
        )

    if name == "run_tests":
        return tools.run_tests()
    if name == "edit_file":
        return tools.edit_file(
            arguments["path"],
            arguments["content"],
        )

    if name == "git_diff":
        return tools.git_diff()

    if name == "git_status":
        return tools.git_status()

    return {
        "error": f"Unknown tool: {name}"
    }

# ==================================================
# Agent
# ==================================================

def run_agent():
    test_output = sys.stdin.read()

    instructions = """
You are an autonomous DevOps troubleshooting agent.

Your task is to investigate a failed CI pipeline and
make the smallest safe code change necessary to fix it.

IMPORTANT RULES:

1. First understand the repository.
2. Use list_files before making assumptions.
3. Read relevant source and test files.
4. Analyze the CI failure.
5. Modify ONLY application source code.
6. NEVER modify tests.
7. NEVER modify GitHub Actions.
8. NEVER modify requirements.txt.
9. Do not add dependencies.
10. Use edit_file only when you have identified a concrete bug.
11. After editing, ALWAYS run the tests.
12. If tests fail, inspect the failure and try another fix.
13. Use git_diff before finishing.
14. Stop after a maximum of 3 edit attempts.
15. If tests pass, report success.
16. If you cannot safely fix the issue, stop and explain why.

You have access to repository tools.
Use them instead of guessing.
"""

    input_items = [
        {
            "role": "user",
            "content": (
                "The CI pipeline failed.\n\n"
                "Initial CI output:\n\n"
                f"{test_output}"
            ),
        }
    ]

    for iteration in range(10):

        print(
            f"\n========== AGENT ITERATION {iteration + 1} ==========\n"
        )

        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            tools=TOOL_DEFINITIONS,
            input=input_items,
        )

        # Preserve the model response for the next turn.
        input_items += response.output

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tools means the model has finished.
        if not tool_calls:

            print("\n========== AGENT FINAL RESPONSE ==========\n")

            print(response.output_text)

            return 0

        for tool_call in tool_calls:

            print(
                f"AI TOOL CALL: {tool_call.name}"
            )

            try:

                arguments = json.loads(
                    tool_call.arguments
                )

                print(
                    f"Arguments: {arguments}"
                )

                result = execute_tool(
                    tool_call.name,
                    arguments,
                )

            except Exception as exc:

                result = {
                    "error": str(exc)
                }

            print(
                f"Tool result: {str(result)[:3000]}"
            )

            input_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(
                        result
                    ),
                }
            )

    print(
        "Agent stopped because maximum iterations were reached."
    )

    return 1


if __name__ == "__main__":
    sys.exit(run_agent())
