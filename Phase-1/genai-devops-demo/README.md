# GenAI DevOps Demo

A small Python project demonstrating basic arithmetic functions with automated tests and a GitHub Actions CI workflow.

## Features

- `add(a, b)` returns the sum of two values.
- `multiply(a, b)` returns the product of two values.
- Pytest tests cover both functions.
- GitHub Actions runs the test suite on pushes to `main` and on pull requests, using Python 3.12.

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
