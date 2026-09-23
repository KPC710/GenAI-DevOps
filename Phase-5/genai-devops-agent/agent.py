import json
import os
import sys

from openai import OpenAI

from config import (
    OPENAI_MODEL,
    MAX_AGENT_ITERATIONS
)

from tools import (
    list_files,
    read_file,
    edit_file,
    run_tests,
    git_diff,
    git_status
)

from rag import search_knowledge

from github_tools import (
    get_workflow_runs,
    get_pull_requests
)


# --------------------------------------------------
# OpenAI client
# --------------------------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# --------------------------------------------------
# Tool definitions
# --------------------------------------------------

TOOL_DEFINITIONS = [

    {
        "type": "function",
        "name": "list_files",
        "description": "List files in the repository.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "read_file",
        "description": "Read a repository file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string"
                }
            },
            "required": [
                "file_path"
            ],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "edit_file",
        "description": "Modify an allowed repository file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                }
            },
            "required": [
                "file_path",
                "content"
            ],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "run_tests",
        "description": "Run pytest.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "git_diff",
        "description": "Show current git changes.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "git_status",
        "description": "Show git status.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "search_knowledge",
        "description": "Search internal DevOps documentation.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": [
                "query"
            ],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "get_workflow_runs",
        "description": "Get recent GitHub Actions workflow runs.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    },

    {
        "type": "function",
        "name": "get_pull_requests",
        "description": "Get recent GitHub pull requests.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
]


# --------------------------------------------------
# Tool router
# --------------------------------------------------

def execute_tool(
    tool_name,
    arguments
):

    if tool_name == "list_files":
        return list_files()

    if tool_name == "read_file":
        return read_file(
            arguments["file_path"]
        )

    if tool_name == "edit_file":
        return edit_file(
            arguments["file_path"],
            arguments["content"]
        )

    if tool_name == "run_tests":
        return run_tests()

    if tool_name == "git_diff":
        return git_diff()

    if tool_name == "git_status":
        return git_status()

    if tool_name == "search_knowledge":
        return search_knowledge(
            arguments["query"]
        )

    if tool_name == "get_workflow_runs":
        return get_workflow_runs()

    if tool_name == "get_pull_requests":
        return get_pull_requests()

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}"
    }


# --------------------------------------------------
# Agent instructions
# --------------------------------------------------

INSTRUCTIONS = """
You are a DevOps software repair agent.

Your job is to investigate CI/CD failures and safely repair
application code.

Follow these rules:

1. Understand the CI failure first.
2. Inspect the repository.
3. Read relevant source files.
4. Read relevant tests.
5. Search internal documentation when useful.
6. Determine the root cause.
7. Make the smallest safe application-code change.
8. NEVER modify tests.
9. NEVER modify GitHub workflows.
10. NEVER modify requirements unless explicitly instructed.
11. Run tests after every modification.
12. If tests fail, investigate and retry.
13. Do not make more than 3 repair attempts.
14. Inspect git diff before finishing.
15. Never expose or create secrets.
16. Never execute destructive commands.
17. Never access files outside the repository.
18. Stop and report if you are uncertain.

Your final response must contain:

- Root cause
- Files changed
- Tests executed
- Test result
- Explanation
"""


# --------------------------------------------------
# Agent
# --------------------------------------------------

def run_agent(error_log):

    input_items = [

        {
            "role": "user",
            "content": f"""
CI/CD pipeline failure:

{error_log}

Investigate and repair the failure.
"""
        }

    ]

    for iteration in range(
        MAX_AGENT_ITERATIONS
    ):

        response = client.responses.create(

            model=OPENAI_MODEL,

            instructions=INSTRUCTIONS,

            tools=TOOL_DEFINITIONS,

            input=input_items
        )

        input_items.extend(
            response.output
        )

        tool_calls = [

            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:

            return response.output_text

        for tool_call in tool_calls:

            try:

                arguments = json.loads(
                    tool_call.arguments
                )

                result = execute_tool(
                    tool_call.name,
                    arguments
                )

            except Exception as exc:

                result = {
                    "success": False,
                    "error": str(exc)
                }

            input_items.append({

                "type":
                    "function_call_output",

                "call_id":
                    tool_call.call_id,

                "output":
                    json.dumps(
                        result
                    )
            })

    return "Agent stopped: maximum iterations reached."


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    error_log = sys.stdin.read()

    if not error_log.strip():

        print(
            "No CI error log provided."
        )

        sys.exit(1)

    try:

        result = run_agent(
            error_log
        )

        print(result)

    except Exception as exc:

        print(
            f"Agent failed: {exc}"
        )

        sys.exit(1)