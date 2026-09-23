from pathlib import Path
import subprocess


# --------------------------------------------------
# Repository root
# --------------------------------------------------

REPO_ROOT = Path.cwd().resolve()


# --------------------------------------------------
# Files that AI is allowed to modify
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".md",
    ".txt",
}


PROTECTED_FILES = {
    "test_app.py",
    "requirements.txt",
    ".github/workflows/ai-devops.yml",
}


# --------------------------------------------------
# Safe path validation
# --------------------------------------------------

def safe_path(file_path: str) -> Path:

    path = (REPO_ROOT / file_path).resolve()

    if not str(path).startswith(str(REPO_ROOT)):
        raise ValueError(
            "Access outside repository is not allowed."
        )

    return path


# --------------------------------------------------
# List repository files
# --------------------------------------------------

def list_files():

    files = []

    for file in REPO_ROOT.rglob("*"):

        if file.is_file():

            relative = file.relative_to(REPO_ROOT)

            # Ignore Git internals
            if ".git" in relative.parts:
                continue

            files.append(str(relative))

    return files


# --------------------------------------------------
# Read file
# --------------------------------------------------

def read_file(file_path: str):

    path = safe_path(file_path)

    if not path.exists():
        return {
            "success": False,
            "error": f"File does not exist: {file_path}"
        }

    return {
        "success": True,
        "file": file_path,
        "content": path.read_text(
            encoding="utf-8"
        )
    }


# --------------------------------------------------
# Edit file
# --------------------------------------------------

def edit_file(
    file_path: str,
    content: str
):

    path = safe_path(file_path)

    relative_path = str(
        path.relative_to(REPO_ROOT)
    )

    # Never allow protected files
    if relative_path in PROTECTED_FILES:

        return {
            "success": False,
            "error": (
                f"Modification blocked. "
                f"{relative_path} is protected."
            )
        }

    # Only allow specific file types
    if path.suffix not in ALLOWED_EXTENSIONS:

        return {
            "success": False,
            "error": (
                f"File extension {path.suffix} "
                f"is not allowed."
            )
        }

    path.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "message": f"{file_path} updated successfully."
    }


# --------------------------------------------------
# Run tests
# --------------------------------------------------

def run_tests():

    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


# --------------------------------------------------
# Git diff
# --------------------------------------------------

def git_diff():

    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "diff": result.stdout
    }


# --------------------------------------------------
# Git status
# --------------------------------------------------

def git_status():

    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "status": result.stdout
    }