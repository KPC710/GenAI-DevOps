# Phase 2: GenAI-Assisted DevOps CI/CD

Phase 2 extends the Phase 1 Python CI pipeline with GenAI-assisted failure analysis. When a test fails, the workflow captures the pytest output, sends it to a Python analyzer backed by the OpenAI API, and publishes the analysis as a GitHub Actions artifact.

## CI/CD Pipeline

```text
Git Push
    |
    v
GitHub Actions
    |
    v
Run tests
    |
  +---+---+
  |       |
 PASS    FAIL
  |       |
  v       v
 Done   Capture logs
            |
            v
     Analyze failure with GenAI
            |
            v
     AI analyzes test-output.txt
            |
            v
       AI analysis artifact
            |
            v
       Pipeline fails
```

The current workflow is started manually with `workflow_dispatch`. The pipeline still represents the normal developer-to-CI flow: a code change is sent to GitHub, tests run, and failures are analyzed before the job is marked failed.

## Developer-to-GenAI Flow

```text
                 DEVELOPER
                     |
                     | git push
                     v
                  GITHUB
                     |
                     v
              GITHUB ACTIONS
                     |
              +------+------+
              |             |
              v             v
          Run Tests       Code
              |          Review
        +-----+-----+
        |           |
       PASS        FAIL
        |           |
        v           v
       Done     Capture Logs
                    |
                    v
              Python Analyzer
                    |
                    v
               OpenAI API
                    |
                    v
                 GenAI
                    |
                    v
              Root Cause
              Recommended Fix
              Corrected Code
                    |
                    v
              GitHub Artifact
```

## Example Failure Analysis

The Phase 2 test intentionally exposes a defect in `multiply()`:

- **Root cause:** `multiply(2, 3)` returns `5` instead of `6`.
- **Failed test:** `test_app.py::test_multiply`.
- **Likely problem:** The implementation uses `a + b` instead of `a * b`.
- **Recommended fix:** Return `a * b` from `multiply()`.
- **Corrected code:**

```python
def multiply(a, b):
    return a * b
```

The analyzer also recommends parameterized tests for positive, negative, zero, and floating-point inputs.

## Phase 2 Concept

**CI/CD produces the problem -> GenAI interprets the problem -> GenAI produces useful information.**

## Requirements

- Python 3.12
- pip
- An `OPENAI_API_KEY` GitHub Actions secret for GenAI analysis

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest -v
```

The GitHub Actions workflow is located at `.github/workflows/main-phase-2-ci.yml`.
