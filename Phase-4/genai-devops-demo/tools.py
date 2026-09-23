import subprocess
from pathlib import Path

# --------------------------------------------------
# Security
# --------------------------------------------------
ALLOWED_EXTENSIONS = {
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".md",
}

PROTECTED_FILES = {
    ".github/workflows/ai-devops.yml",
    "requirements.txt",
    "test_app.py",
}

def safe_path(path):
    """
    Prevent the agent from accessing files outside
    the repository.
    """

    root = Path.cwd().resolve()
    target = (root / path).resolve()

    if root not in target.parents and target != root:
        raise ValueError("Unsafe path detected")

    return target

# --------------------------------------------------
# Tool 1: List files
# --------------------------------------------------

def list_files():
    files = []

    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        files.append(str(path))

    return files

# --------------------------------------------------
# Tool 2: Read file
# --------------------------------------------------

def read_file(path):
    target = safe_path(path)
    if not target.exists():
        return f"File does not exist: {path}"
    if not target.is_file():
        return f"Not a file: {path}"
    return target.read_text(encoding="utf-8")

# --------------------------------------------------
# Tool 3: Run tests
# --------------------------------------------------

def run_tests():
    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True,
        timeout=120,
    )

    return {
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

# --------------------------------------------------
# Tool 4: Edit file
# --------------------------------------------------

def edit_file(path, content):
    if path in PROTECTED_FILES:
        return {
            "success": False,
            "error": f"Modification blocked for protected file: {path}",
        }

    target = safe_path(path)

    if target.suffix not in ALLOWED_EXTENSIONS:
        return {
            "success": False,
            "error": f"File type not allowed: {target.suffix}",
        }

    target.write_text(
        content,
        encoding="utf-8",
    )

    return {
        "success": True,
        "message": f"Updated {path}",
    }

# --------------------------------------------------
# Tool 5: Git diff
# --------------------------------------------------

def git_diff():

    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True,
    )

    return result.stdout

# --------------------------------------------------
# Tool 6: Git status
# --------------------------------------------------

def git_status():

    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
    )

    return result.stdout
