# Phase 5: RAG-Enabled GenAI DevOps Agent

Phase 5 combines the previous CI/CD and autonomous remediation stages into a broader DevOps agent architecture. The agent can inspect the repository, run tests, modify approved application code, search internal documentation, inspect GitHub workflow runs and pull requests, use MCP-based documentation tools, and prepare a pull request after a successful repair.

## Complete Architecture

```text
                     DEVELOPER
                         |
                         | git push
                         v
                    +---------+
                    | GitHub  |
                    +----+----+
                         |
                         v
                +-----------------+
                | GitHub Actions  |
                +--------+--------+
                         |
                         v
                    Run pytest
                         |
                  +------+------+
                  |             |
                PASS           FAIL
                  |             |
                  v             v
                Done        AI AGENT
                              |
                    +---------+----------+
                    |         |          |
                    v         v          v
                 Tools      RAG       GitHub
                    |         |          |
                    v         v          v
                tools.py   rag.py   github_tools.py
                    |
                    v
              Read app.py
                    |
                    v
              Understand bug
                    |
                    v
              Modify app.py
                    |
                    v
                Run pytest
                    |
              +-----+-----+
              |           |
            FAIL        PASS
              |           |
              v           v
          Retry       git diff
                          |
                          v
                     Create branch
                          |
                          v
                        Push
                          |
                          v
                     Create PR
                          |
                          v
                   Human Review
```

A passing original test suite completes normally. A failing test suite starts the agent. The agent investigates the failure, makes a guarded application-code change, verifies the change, and creates a pull request only after the tests pass.

## Project Files

| File or directory | Purpose | Capability |
| --- | --- | --- |
| `app.py` | Application code under test | Foundation |
| `test_app.py` | Automated tests | Foundation |
| `requirements.txt` | Python dependencies | Foundation |
| `gitignore` | Git exclusions for the project | Foundation |
| `config.py` | Model, limits, allowed files, and protected files | Agent foundation |
| `tools.py` | Safe repository tools used by the agent | Agent |
| `agent.py` | LLM-driven orchestrator and tool loop | GenAI agent |
| `rag.py` | Local knowledge retrieval from Markdown files | RAG |
| `github_tools.py` | GitHub CLI and repository operations | DevOps automation |
| `mcp_server.py` | Standardized MCP documentation tools | MCP |
| `knowledge/*.md` | Internal DevOps documentation | RAG |
| `.github/workflows/main-phase-5-ci-agent.yml` | CI/CD automation | GitHub Actions |

## The Agent Brain, Hands, Memory, and GitHub

The core architecture separates decision-making from capabilities:

```text
                         +----------------+
                         |      LLM       |
                         |     BRAIN      |
                         +--------+-------+
                                  |
                          decides what to do
                                  |
             +--------------------+--------------------+
             v                    v                    v
         tools.py              rag.py          github_tools.py
          HANDS                 MEMORY              GITHUB
             |                    |                    |
             v                    v                    v
       Files and tests       Company docs        GitHub API/CLI
```

- `agent.py` is the orchestrator. It sends the failure context to the LLM, receives tool calls, executes them, and returns each result to the next model iteration.
- `tools.py` gives the agent controlled access to repository files, tests, status, and diffs.
- `rag.py` gives the agent searchable internal knowledge from the local `knowledge/` directory.
- `github_tools.py` gives the agent access to workflow runs, pull requests, branches, and GitHub operations.

The LLM decides which capability to use. The Python functions enforce what each capability is allowed to do.

## Agent Tool Loop

```text
AI
 |
 +-- list_files()
 |
 +-- read_file("app.py")
 |
 +-- read_file("test_app.py")
 |
 +-- search_knowledge("pytest failure")
 |
 +-- get_workflow_runs()
 |
 +-- Analyze
 |
 +-- edit_file("app.py", ...)
 |
 +-- run_tests()
 |
 +-- git_diff()
 |
 +-- git_status()
 |
 +-- Finish or retry
```

The agent works in iterations. Each iteration can contain one or more tool calls. The result of every tool call is sent back to the model so it can decide the next action based on the actual repository state.

The agent is instructed to:

1. Understand the CI failure first.
2. Inspect files and tests before editing.
3. Search internal documentation when useful.
4. Make the smallest safe application-code change.
5. Never modify tests, workflows, or dependencies.
6. Run tests after every modification.
7. Inspect the final Git diff.
8. Stop after the configured iteration and repair limits.

## Example Execution

```text
========== AGENT ITERATION 1 ==========

AI TOOL CALL: list_files

AI TOOL CALL: read_file
Arguments:
{"file_path":"app.py"}

AI TOOL CALL: read_file
Arguments:
{"file_path":"test_app.py"}

========== AGENT ITERATION 2 ==========

AI TOOL CALL: search_knowledge
Arguments:
{"query":"pytest failure arithmetic function"}

========== AGENT ITERATION 3 ==========

AI TOOL CALL: edit_file
Arguments:
{
    "file_path":"app.py",
    "content":"..."
}

========== AGENT ITERATION 4 ==========

AI TOOL CALL: run_tests

========== AGENT ITERATION 5 ==========

AI TOOL CALL: git_diff
```

A typical failure remediation is:

```text
Failure
   |
   v
Read app.py
   |
   v
Read test_app.py
   |
   v
Search internal knowledge
   |
   v
Send context to AI
   |
   v
AI returns a repair action
   |
   v
Modify app.py
   |
   v
Run pytest
   |
   +-- FAIL -> inspect and retry
   |
   +-- PASS -> git_diff -> branch -> push -> PR
```

## Tools

### Repository tools: `tools.py`

`tools.py` provides the agent’s controlled hands:

- `list_files()` lists repository files while ignoring Git internals.
- `read_file(path)` reads a repository file after path validation.
- `edit_file(path, content)` writes approved file types while protecting tests, dependencies, and workflows.
- `run_tests()` executes pytest and returns success, exit code, standard output, and standard error.
- `git_diff()` returns the current uncommitted changes.
- `git_status()` returns the working-tree status.

The tools resolve paths inside the repository and reject attempts to access files outside it.

### Retrieval-Augmented Generation: `rag.py`

`rag.py` searches the local `knowledge/` directory. It loads Markdown documents, compares query words with document words, ranks matches by overlap, and returns the top results.

The knowledge base contains DevOps documentation such as:

- `knowledge/architecture.md`
- `knowledge/deployment.md`
- `knowledge/troubleshooting.md`

This gives the agent project-specific context instead of relying only on general model knowledge.

### GitHub integration: `github_tools.py`

`github_tools.py` wraps GitHub CLI and Git operations for DevOps automation. It can:

- Read the current repository from `GITHUB_REPOSITORY`.
- List recent GitHub Actions workflow runs.
- List and inspect pull requests.
- Create a branch from the current commit.
- Push a branch to the repository.
- Create a pull request against `main`.

GitHub operations return structured success or error results so the agent can reason about failures.

## RAG and MCP

There are two related but separate documentation concepts:

### RAG: `rag.py`

RAG is the agent’s direct local retrieval path. The agent calls `search_knowledge(query)`, which searches the Markdown files in `knowledge/` and returns relevant documentation in the same Python process.

```text
Agent query
    |
    v
rag.py
    |
    v
knowledge/*.md
    |
    v
Relevant documentation
```

### MCP: `mcp_server.py`

MCP exposes documentation as standardized tools through an MCP server. The server provides:

- `search_docs(query)` to search documentation content.
- `list_docs()` to list available documentation files.

```text
MCP client
    |
    v
mcp_server.py
    |
    v
Standardized documentation tools
    |
    v
knowledge/*.md
```

RAG is the agent’s built-in retrieval implementation. MCP is an interoperable tool interface that allows compatible clients to discover and call documentation tools.

## Configuration and Safety

`config.py` centralizes the controls that govern the agent:

```text
                    config.py
                 +------+------+
                 |             |
             Agent limits   Safety rules
                 |             |
                 v             v
          max iterations   protected files
          repair attempts  allowed files
          model selection  confidence limit
```

Important controls include:

- `OPENAI_MODEL` selects the model and defaults to `gpt-5.5` when unset or empty.
- `MAX_AGENT_ITERATIONS` limits the number of model/tool turns.
- `MAX_REPAIR_ATTEMPTS` limits repair attempts.
- `ALLOWED_FILES` identifies files the agent may modify.
- `PROTECTED_FILES` prevents changes to tests, dependencies, and workflows.
- `MIN_CONFIDENCE` defines the minimum safe confidence threshold.

Additional safeguards include path validation, allowed file extensions, post-edit testing, Git diff review, and pull request review before merge.

## GitHub Actions Workflow

The Phase 5 workflow at `.github/workflows/main-phase-5-ci-agent.yml` performs these steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs `requirements.txt`.
4. Runs pytest and captures `ci-output.txt`.
5. Starts `agent.py` only when tests fail.
6. Saves the agent output as `ai-analysis.txt`.
7. Shows the generated changes.
8. Creates and pushes an AI branch after a real `app.py` change.
9. Creates a pull request using the generated analysis.
10. Uploads CI and AI artifacts.

The workflow uses `pipefail` so pytest and agent failures are not hidden by `tee`. It also refuses to create a pull request when the agent produced no `app.py` commit.

Required workflow permissions are:

```yaml
permissions:
  contents: write
  pull-requests: write
  actions: read
```

GitHub must also allow Actions to create and approve pull requests under repository **Settings -> Actions -> General -> Workflow permissions**.

## Local Setup

```bash
cd Phase-5/genai-devops-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

To run the agent using a captured CI failure:

```bash
OPENAI_API_KEY=your-key \
GITHUB_TOKEN=your-token \
GITHUB_REPOSITORY=owner/repository \
python agent.py < ci-output.txt
```

The agent requires `OPENAI_API_KEY` for GenAI calls. GitHub operations also require an authenticated `gh` environment or a token with the necessary repository permissions.

## Phase 5 Outcome

Phase 5 connects the complete DevOps automation loop:

```text
CI failure
    |
    v
Agent investigation
    |
    +-- repository tools
    +-- RAG knowledge
    +-- GitHub data
    +-- MCP documentation interface
    |
    v
Safe application repair
    |
    v
Verified tests
    |
    v
Branch and pull request
    |
    v
Human review
```

The LLM is the decision-making brain, the tools are its controlled hands, RAG is its project memory, GitHub integration is its DevOps interface, and MCP provides a standardized path for external documentation tools.
