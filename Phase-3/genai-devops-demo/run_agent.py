import json
import subprocess
import sys
from pathlib import Path

from ai_agent import analyze_failure

ALLOWED_FILES = {
    "app.py",
}
PROJECT_DIR = Path(__file__).resolve().parent

def run_tests():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        capture_output=True,
        text=True,
    )
    output = result.stdout + "\n" + result.stderr
    if not output.strip():
        output = f"pytest exited with code {result.returncode} without producing output."
    return result.returncode, output

def apply_fix(result):

    file_to_modify = result.get("file_to_modify")
    replacement = result.get("replacement")
    confidence = result.get("confidence", 0)

    print(f"AI confidence: {confidence}")
    print(f"AI wants to modify: {file_to_modify}")

    if confidence < 0.80:
        raise RuntimeError(
            "AI confidence is below the safe threshold."
        )
    if not isinstance(file_to_modify, str):
        raise RuntimeError("AI did not provide a valid file path.")

    requested_path = Path(file_to_modify)
    allowed_path = (PROJECT_DIR / "app.py").resolve()
    candidate_paths = [requested_path]
    if not requested_path.is_absolute():
        candidate_paths.extend(
            [
                Path.cwd() / requested_path,
                PROJECT_DIR / requested_path,
                PROJECT_DIR.parents[1] / requested_path,
            ]
        )

    target_path = next(
        (
            candidate.resolve()
            for candidate in candidate_paths
            if candidate.resolve() == allowed_path
        ),
        None,
    )

    if target_path is None or Path(file_to_modify).name not in ALLOWED_FILES:
        raise RuntimeError(
            f"File modification not allowed: {file_to_modify}"
        )
    if not replacement:
        raise RuntimeError(
            "AI did not provide replacement code."
        )
    target_path.write_text(
        replacement,
        encoding="utf-8",
    )
    print(f"Applied AI fix to {target_path}")

def main():

    print("======================================")
    print(" GenAI DevOps Autonomous Agent")
    print("======================================")

    print("\nRunning tests...")

    exit_code, test_output = run_tests()

    if exit_code == 0:
        print("Tests already pass.")
        return 0

    print("\nTests failed.")
    print(f"Captured test output ({len(test_output)} characters).")
    print("\nSending failure to GenAI...\n")

    try:
        result = analyze_failure(test_output)
    except Exception as exc:
        print(f"AI analysis failed: {exc}")
        return 1

    print("\nAI ANALYSIS")
    print("-----------")
    print(json.dumps(result, indent=2))

    try:
        apply_fix(result)
    except Exception as exc:
        print(f"\nUnsafe AI fix rejected: {exc}")
        return 1

    print("\nRunning tests after AI fix...")
    exit_code, new_output = run_tests()
    print(new_output)

    if exit_code != 0:
        print("AI fix did not resolve the failure.")
        return 1

    print("\n======================================")
    print(" AI FIX SUCCESSFUL")
    print("======================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
