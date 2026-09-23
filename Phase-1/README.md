# Phase 1: DevOps CI/CD

This phase demonstrates a normal DevOps CI/CD workflow for a Python application.

## CI/CD Pipeline

```text
Git Push
    |
    v
GitHub Actions
    |
    v
Checkout Code
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
  +---+---+
  |       |
 PASS    FAIL
  |       |
  v       v
  ✅      ❌
```

The workflow checks out the code, configures Python, installs the project dependencies, and runs the test suite. A passing test suite completes the pipeline successfully; a failing test suite marks the pipeline as failed.

## Project

The sample Python application is in [genai-devops-demo](genai-devops-demo/).
