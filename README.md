# GenAI DevOps

An evolving DevOps platform that combines Python development, GitHub Actions, GenAI-powered failure analysis, and tool-using autonomous agents.

The project starts with a conventional CI pipeline and progressively adds intelligence and automation: first testing code, then explaining failures, then safely applying fixes and preparing them for human review.

## Project Vision

```text
Developer -> GitHub -> GitHub Actions -> Tests
					    |
					    v
				   Failure analysis
					    |
					    v
				     GenAI Agent
					    |
					    v
			     Safe code remediation
					    |
					    v
				  Pull request review
```

The central principle is simple:

> CI/CD produces the engineering problem. GenAI interprets the problem. Automation produces useful, reviewable engineering information.

## Capability Progression

```text
LEVEL 1
Python + Git + GitHub
	  |
	  v
LEVEL 2
GitHub Actions / CI/CD
	  |
	  v
LEVEL 3
GenAI API
	  |
	  v
LEVEL 4
GenAI analyzes CI failures
	  |
	  v
LEVEL 5
AI Agent + Tools
	  |
	  v
LEVEL 6
GitHub API
	  |
	  v
LEVEL 7
Automatic PR creation
	  |
	  v
LEVEL 8
RAG + documentation
	  |
	  v
LEVEL 9
MCP
	  |
	  v
LEVEL 10
Multi-step autonomous DevOps agent
```

The completed project demonstrates the foundation through tool-using DevOps automation: Python applications, Git workflows, CI/CD, GenAI analysis, guarded code changes, test verification, branch creation, pull requests, and human review.

## Current Project Structure

```text
GenAI/
|
+-- README.md
+-- .github/
|   +-- workflows/
|       +-- main-phase-1-ci.yml
|       +-- main-phase-2-ci.yml
|       +-- main-phase-3-ci.yml
|       +-- main-phase-4-ci.yml
|
+-- Phase-1/
|   +-- genai-devops-demo/
|       +-- app.py
|       +-- test_app.py
|       +-- requirements.txt
|       +-- README.md
|
+-- Phase-2/
|   +-- genai-devops-demo/
|       +-- app.py
|       +-- test_app.py
|       +-- ai_analyzer.py
|       +-- requirements.txt
|       +-- README.md
|
+-- Phase-3/
|   +-- genai-devops-demo/
|       +-- app.py
|       +-- test_app.py
|       +-- ai_agent.py
|       +-- run_agent.py
|       +-- requirements.txt
|       +-- README.md
|
+-- Phase-4/
    +-- genai-devops-demo/
	  +-- app.py
	  +-- test_app.py
	  +-- agent.py
	  +-- tools.py
	  +-- requirements.txt
	  +-- README.md

+-- Phase-5/
    +-- genai-devops-agent/
	  +-- app.py
	  +-- test_app.py
	  +-- agent.py
	  +-- tools.py
	  +-- config.py
	  +-- rag.py
	  +-- github_tools.py
	  +-- mcp_server.py
	  +-- knowledge/
	  +-- requirements.txt
	  +-- README.md
```

## Phase 1: Conventional CI/CD

Phase 1 establishes the basic Python delivery pipeline.

```text
Git Push
    |
    v
GitHub Actions
    |
    v
Checkout code
    |
    v
Setup Python
    |
    v
Install dependencies
    |
    v
Run pytest
    |
    v
PASS or FAIL
```

The application contains simple arithmetic functions and tests. GitHub Actions checks out the repository, configures Python 3.12, installs `requirements.txt`, and runs pytest from the Phase 1 project directory.

This phase establishes the basic feedback loop: every code change can be checked by an automated test suite.

Read the detailed [Phase 1 README](Phase-1/genai-devops-demo/README.md).

## Phase 2: GenAI Failure Analysis

Phase 2 adds an analysis stage after a failed test run.

```text
Run tests
    |
    v
  FAIL
    |
    v
Capture test-output.txt
    |
    v
Analyze failure with GenAI
    |
    v
Create ai-analysis.txt
    |
    v
Upload analysis artifact
    |
    v
Fail the pipeline
```

The workflow preserves the pytest failure with shell `pipefail`, sends the captured output to `ai_analyzer.py`, and stores the analysis together with the test output as a GitHub Actions artifact.

The analysis explains:

- The root cause.
- The failed test.
- The likely problem.
- The recommended fix.
- Corrected code.
- Prevention recommendations.

The pipeline still fails after analysis. GenAI explains the problem, but the developer remains responsible for applying the fix.

Read the detailed [Phase 2 README](Phase-2/genai-devops-demo/README.md).

## Phase 3: Autonomous Remediation Agent

Phase 3 moves from explanation to guarded code remediation.

```text
CI test failure
	 |
	 v
Read failure output, source, and tests
	 |
	 v
Send context to GenAI
	 |
	 v
Receive structured remediation
	 |
	 v
Validate confidence and target file
	 |
	 v
Modify app.py
	 |
	 v
Run tests again
	 |
   +---+---+
   |       |
 FAIL    PASS
   |       |
 STOP    Create branch and PR
```

The Phase 3 agent:

1. Runs the test suite and captures the failure.
2. Reads the application and test source.
3. Sends the context to the GenAI API.
4. Requires a structured JSON remediation response.
5. Checks the confidence threshold.
6. Allows changes only to `app.py`.
7. Applies the complete replacement code.
8. Runs the tests again.
9. Creates a branch and pull request only after the tests pass.

This phase introduces a human approval boundary. The agent can prepare a change, but it does not merge code directly into `main`.

Read the detailed [Phase 3 README](Phase-3/genai-devops-demo/README.md).

## Phase 4: Tool-Using GenAI Agent

Phase 4 gives the agent explicit repository tools so it can investigate before acting.

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

The agent can decide which tool to call and when:

```text
list_files()
	|
	v
read_file("app.py")
	|
	v
read_file("test_app.py")
	|
	v
Analyze failure
	|
	v
edit_file("app.py", ...)
	|
	v
run_tests()
	|
	v
git_diff()
	|
	v
Finish or continue
```

The agent is iterative rather than a single prompt-and-response script. It receives tool results, considers the next action, and continues until the tests pass, the safety rules reject the operation, or the iteration limit is reached.

Read the detailed [Phase 4 README](Phase-4/genai-devops-demo/README.md).

## Phase 5: RAG-Enabled DevOps Agent

Phase 5 connects the complete architecture: GitHub Actions, a tool-using AI agent, local documentation retrieval, GitHub automation, and an MCP documentation server.

```text
Developer -> GitHub -> GitHub Actions -> pytest
						  |
						  v
					     AI Agent
						  |
			  +-----------------+-----------------+
			  |                 |                 |
		     tools.py          rag.py       github_tools.py
		     Files/tests     Knowledge       GitHub API/CLI
						  |
						  v
					 Repair app.py
						  |
						  v
					  Run pytest
						  |
						  v
				     Branch -> Push -> PR
						  |
						  v
					  Human Review
```

The Phase 5 agent can inspect repository files, search internal DevOps documentation, examine workflow runs and pull requests, modify approved application code, rerun tests, review the Git diff, and create a pull request after a successful repair.

The architecture separates responsibilities:

- `agent.py` is the LLM-driven orchestrator and decides which tool to call next.
- `tools.py` provides safe file, test, status, and diff operations.
- `rag.py` searches Markdown files in `knowledge/` for project-specific context.
- `github_tools.py` connects the agent to GitHub CLI and repository operations.
- `mcp_server.py` exposes documentation through standardized MCP tools.
- `config.py` defines model selection, iteration limits, repair limits, protected files, and confidence rules.

RAG and MCP serve different purposes. RAG is the agent's direct local search over `knowledge/*.md`; MCP exposes documentation capabilities as interoperable tools for compatible clients.

The workflow creates a branch and pull request only when the agent produces a real `app.py` change and the verification flow succeeds. Tests, dependencies, and workflow files remain protected, and a human reviews the resulting pull request.

Read the detailed [Phase 5 README](Phase-5/genai-devops-agent/README.md).

## Tool Responsibilities

| Tool | Responsibility |
| --- | --- |
| `list_files()` | Understand the repository structure before making assumptions. |
| `read_file(path)` | Inspect source code, tests, configuration, and documentation. |
| `run_tests()` | Execute pytest and return output and exit status. |
| `edit_file(path, content)` | Apply a complete source-file replacement after a concrete diagnosis. |
| `git_diff()` | Review the exact uncommitted changes. |
| `git_status()` | Check the working-tree state. |
| Create PR | Publish a successful fix for human review. |

## Safety Model

Automation is constrained at several boundaries:

- Test files cannot be edited by the agent.
- GitHub Actions workflows cannot be edited by the agent.
- Dependency files cannot be edited by the agent.
- File paths are checked to prevent access outside the repository.
- Only approved file extensions can be changed.
- The agent must run tests after editing.
- A confidence threshold is required before applying a proposed fix.
- The final code change is sent to a pull request instead of merged automatically.
- GitHub Actions preserves test failures with `pipefail` so failures cannot be hidden by log capture.

## GitHub Actions Flow

Each phase has a dedicated workflow under `.github/workflows/`. The workflows use a project-specific working directory so dependency installation and tests run against the correct phase.

The Phase 3, Phase 4, and Phase 5 workflows require:

```yaml
permissions:
  contents: write
  pull-requests: write
```

The repository must also allow GitHub Actions to create and approve pull requests under **Settings -> Actions -> General -> Workflow permissions**.

## Local Development

Each phase is an independent Python project with its own dependencies and README. To work on a phase:

```bash
cd Phase-5/genai-devops-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

To run the tool-using agent with captured CI output:

```bash
OPENAI_API_KEY=your-key python agent.py < ci-output.txt
```

The GitHub Actions environment supplies `OPENAI_API_KEY` through repository secrets and selects the model with `OPENAI_MODEL`.

## End-to-End Outcome

The project demonstrates the progression from a basic automated test to an agent that can investigate and prepare a code change:

```text
Developer change
	|
	v
Automated CI test
	|
	v
Failure captured
	|
	v
GenAI explanation
	|
	v
Tool-using investigation
	|
	v
Guarded code change
	|
	v
Verification with pytest
	|
	v
Pull request
	|
	v
Human review and merge
```

The result is a practical DevOps feedback loop in which automation speeds up diagnosis and remediation while testing, safety controls, and human review preserve engineering accountability.
