# GenAI DevOps Demo

A small Python project demonstrating basic arithmetic functions with automated tests and a GitHub Actions CI workflow.

## CI/CD Pipeline

This project demonstrates a normal DevOps CI/CD workflow for a Python application:

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

## Features

- `add(a, b)` returns the sum of two values.
- `multiply(a, b)` returns the product of two values.
- Pytest tests cover both functions.
- GitHub Actions runs the test suite with Python 3.12 when manually triggered.

## Requirements

- Python 3.12 (the CI workflow uses this version)
- pip

## Setup

Clone the repository, then from the project directory create and activate a virtual environment and install the requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the tests

```bash
pytest
```

## Use the functions

```python
from app import add, multiply

print(add(2, 3))       # 5
print(multiply(2, 3))  # 6
```
