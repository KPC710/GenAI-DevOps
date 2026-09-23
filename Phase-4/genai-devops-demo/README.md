# Phase 4: Tool-Using GenAI DevOps Agent

Phase 4 introduces a GenAI agent that can inspect a repository, run tests, edit application code, review its own changes, and create a pull request after a successful fix. The AI decides which tool to call and when, while the workflow and tool layer enforce the repository boundaries.

## Target Architecture

```text
GitHub Actions
      |
      v
   AI Agent
      |
      +-- list_files()
      +-- read_file()
      +-- run_tests()
      +-- edit_file()
      +-- git_diff()
      +-- git_status()
      +-- create PR
             |
             v
        Human Review
```

The agent does not directly merge changes. It creates a branch and pull request after tests pass, leaving the final decision with a human reviewer.

## Repository Layout

```text
genai-devops-agent/
|
+-- app.py
+-- test_app.py
+-- requirements.txt
+-- agent.py
+-- tools.py
|
+-- .github/
    +-- workflows/
```

In this repository, the Phase 4 project is located at `Phase-4/genai-devops-demo/`, and its workflow is `.github/workflows/main-phase-4-ci.yml`.

## Agent Decision Loop

```text
             AI
              |
       +------+-------+
       v      v       v
    Read    Edit    Test
       |      |       |
       +------+-------+
              v
           Decide
              |
              v
         Next action
```

The AI determines which tool to call and when. It can inspect the repository before making assumptions, apply a minimal application-code change, run the tests, and inspect the resulting diff before finishing.

## Example Agent Flow

```text
AI
 |
 +-- list_files()
 |
 +-- read_file("app.py")
 |
 +-- read_file("test_app.py")
 |
 +-- Analyze
 |
 +-- edit_file("app.py", ...)
 |
 +-- run_tests()
 |
 +-- Tests PASS
 |
 +-- git_diff()
 |
 +-- Finish
```

A typical execution appears as the following iterations:

```text
========== AGENT ITERATION 1 ==========

AI TOOL CALL: list_files

AI TOOL CALL: read_file
Arguments:
{"path":"app.py"}

AI TOOL CALL: read_file
Arguments:
{"path":"test_app.py"}

========== AGENT ITERATION 2 ==========

AI TOOL CALL: edit_file

Arguments:
{
    "path": "app.py",
    "content": "..."
}

========== AGENT ITERATION 3 ==========

AI TOOL CALL: run_tests

========== AGENT ITERATION 4 ==========

AI TOOL CALL: git_diff
```

## Example Remediation

The original failure is caused by `multiply()` using addition instead of multiplication:

```python
def multiply(a, b):
    return a + b
```

The agent identifies the problem and proposes:

```python
def multiply(a, b):
    return a * b
```

The remediation loop is:

```text
Failure
   |
   v
Read app.py
   |
   v
Send context to AI
   |
   v
AI returns replacement
   |
   v
Modify app.py
   |
   v
Run tests
   |
   v
Tests PASS
```

The agent only finishes successfully after the updated application passes the test suite.

## Available Tools

### `list_files()`

Lists repository files so the agent can understand the project structure.

### `read_file(path)`

Reads source code, tests, configuration, or other repository files needed for diagnosis.

### `run_tests()`

Runs the pytest suite and returns the exit code, standard output, and standard error.

### `edit_file(path, content)`

Replaces a file with complete new content. The tool validates the path and blocks protected files such as tests, workflow files, and dependency definitions.

### `git_diff()`

Shows the uncommitted changes so the agent can review what it modified.

### `git_status()`

Shows the current working-tree status before the agent finishes.

### Create PR

The GitHub Actions workflow creates a branch and opens a pull request when the agent has applied a fix and the tests pass.

## Workflow

1. GitHub Actions checks out the repository and installs the Phase 4 dependencies.
2. The original pytest suite runs and its output is captured.
3. When tests fail, `agent.py` receives the failure output.
4. The agent uses tools to inspect the repository and diagnose the failure.
5. The agent edits application code only when it has identified a concrete fix.
6. The agent reruns the tests and reviews the Git diff.
7. A passing remediation creates an AI branch and pull request.
8. A human reviews and merges the proposed change.

The workflow uses `set -o pipefail` so pytest failures are not hidden by the output capture pipeline. If the agent cannot safely resolve the problem, the workflow fails instead of creating a pull request.

## Safety Boundaries

- Tests cannot be modified by the agent.
- GitHub Actions workflows cannot be modified by the agent.
- `requirements.txt` cannot be modified by the agent.
- Only approved file types can be edited.
- Repository paths are validated to prevent access outside the workspace.
- The agent must run tests after editing.
- Changes are submitted for human review instead of merged automatically.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

To run the agent with captured CI output:

```bash
OPENAI_API_KEY=your-key python agent.py < ci-output.txt
```

The GitHub Actions workflow also requires the repository setting that allows GitHub Actions to create and approve pull requests, in addition to `contents: write` and `pull-requests: write` workflow permissions.
