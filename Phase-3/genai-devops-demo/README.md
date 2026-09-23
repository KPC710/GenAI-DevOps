# Phase 3: GenAI DevOps Autonomous Agent

Phase 3 extends the CI/CD pipeline into an autonomous remediation workflow. When tests fail, a GenAI agent analyzes the application code, test logs, and test definitions, proposes a safe fix, applies the fix only to the permitted application file, reruns the tests, and opens a pull request for human review when the fix succeeds.

## Autonomous Remediation Flow

```text
					Git Push
					   |
					   v
				 GitHub Actions
					   |
					   v
				   Run Tests
					   |
					   v
					FAIL
					   |
					   v
				Collect failure
					   |
					   v
				  GenAI Agent
					   |
			 +---------+---------+
			 |                   |
		Analyze code         Analyze logs
			 |                   |
			 +---------+---------+
					   |
					   v
				 Generate Fix
					   |
					   v
				 Safety Check
					   |
					   v
				 Modify app.py
					   |
					   v
				   Run Tests
					   |
				 +-----+-----+
				 |           |
				FAIL        PASS
				 |           |
				 v           v
			  STOP       Git Branch
							 |
							 v
						Pull Request
							 |
							 v
						  HUMAN
							 |
					   Review & Merge
```

## How It Works

1. **Run tests:** GitHub Actions checks the repository and runs the Phase 3 pytest suite.
2. **Collect the failure:** The agent captures the pytest exit code and complete test output.
3. **Analyze code and logs:** The GenAI agent receives the failure output, `app.py`, and `test_app.py`.
4. **Generate a fix:** The model returns structured JSON containing the root cause, failed test, proposed file, complete replacement code, and confidence score.
5. **Safety check:** The agent requires a confidence of at least `0.80`, accepts only `app.py`, and rejects missing or unsafe replacement content.
6. **Modify the application:** Only the allowed `app.py` file is changed. Tests and workflow files cannot be modified by the agent.
7. **Retest:** The agent runs pytest again after applying the proposed fix.
8. **Stop or create a PR:** A failed retest stops the workflow. A passing retest creates an AI branch and opens a pull request.
9. **Human review:** A developer reviews the generated change before merging it into `main`.

## Three DevOps Levels

### Level 1: Continuous Integration

```text
GitHub -> GitHub Actions -> pytest
```

The pipeline automatically validates code by running tests. A failure stops the pipeline and requires a developer to investigate the issue manually.

### Level 2: GenAI-Assisted CI

```text
CI error -> LLM -> explanation
```

The pipeline sends the test failure to an LLM. The LLM explains the root cause, identifies the failed test, and recommends a correction. The developer still applies the fix manually.

### Level 3: Autonomous DevOps Agent

```text
CI error
	|
	v
   LLM
	|
	v
Understand failure
	|
	v
Generate fix
	|
	v
Apply fix safely
	|
	v
Run tests again
	|
	v
Create pull request
```

The agent performs the remediation loop, but the final code change still requires human review and approval. This keeps automation useful without allowing an unreviewed model response to merge directly into the main branch.

## Safety Controls

- The AI response must match a strict JSON schema.
- The confidence score must be at least `0.80`.
- Only `app.py` is an allowed modification target.
- The replacement must contain complete source code.
- Tests must pass after the change before a pull request is created.
- GitHub Actions creates a branch and pull request instead of merging automatically.

## GitHub Actions Permissions

The workflow requires `contents: write` and `pull-requests: write`. GitHub must also allow Actions to create and approve pull requests:

**Repository Settings -> Actions -> General -> Workflow permissions -> Allow GitHub Actions to create and approve pull requests**

Without this repository setting, the agent can create a branch but the `gh pr create` step will fail.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

The autonomous agent can be run locally with:

```bash
OPENAI_API_KEY=your-key python run_agent.py
```

The GitHub Actions workflow is located at `.github/workflows/main-phase-3-ci.yml`.
