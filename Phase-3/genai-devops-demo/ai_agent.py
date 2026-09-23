import json
import os
import sys
from openai import OpenAI
from pathlib import Path

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
PROJECT_DIR = Path(__file__).resolve().parent
ANALYSIS_SCHEMA = {
    "type": "json_schema",
    "name": "devops_failure_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "root_cause": {"type": "string"},
            "failed_test": {"type": "string"},
            "file_to_modify": {"type": "string"},
            "explanation": {"type": "string"},
            "replacement": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": [
            "root_cause",
            "failed_test",
            "file_to_modify",
            "explanation",
            "replacement",
            "confidence",
        ],
        "additionalProperties": False,
    },
}

def read_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")

def build_prompt(test_output, source_code, test_code):
    prompt = f"""
You are an expert DevOps debugging agent.

A CI pipeline has failed.

Your job is to analyze the failure and propose a SAFE minimal code fix.

The text between TEST OUTPUT BEGIN and TEST OUTPUT END is the authoritative pytest output. Use it to identify the failed test. Do not claim that the failure context is missing unless the section is empty.

TEST OUTPUT BEGIN
{test_output}
TEST OUTPUT END

APPLICATION CODE
----------------
{source_code}

TEST CODE
---------
{test_code}

Return ONLY valid JSON using this exact structure:

{{
  "root_cause": "Explain the root cause",
  "failed_test": "Name of the failed test",
  "file_to_modify": "Relative path of the file to modify",
  "explanation": "Explain the proposed fix",
  "replacement": "Complete corrected content of the file",
  "confidence": 0.0
}}

Rules:

1. Only modify application source code.
2. Do not modify tests.
3. Do not modify GitHub Actions.
4. Do not add dependencies.
5. Make the smallest reasonable fix.
6. The replacement must contain the COMPLETE file.
7. If you cannot determine a safe fix, return confidence below 0.5.
"""

def analyze_failure(test_output):
    if not test_output.strip():
        raise ValueError("Pytest produced no failure output for analysis.")

    client = OpenAI()
    source_code = read_file(PROJECT_DIR / "app.py")
    test_code = read_file(PROJECT_DIR / "test_app.py")
    prompt = str(build_prompt(test_output, source_code, test_code)).strip()
    if not prompt:
        raise ValueError("Generated analysis prompt is empty.")

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a reliable software engineering agent. Analyze the supplied "
            "failed tests and return a safe minimal fix. Do not ask questions."
        ),
        input=prompt,
        text={"format": ANALYSIS_SCHEMA},
    )

    text = response.output_text.strip()

    # Handle accidental markdown fences.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    required_fields = {
        "root_cause",
        "failed_test",
        "file_to_modify",
        "explanation",
        "replacement",
        "confidence",
    }
    missing_fields = required_fields - result.keys()
    if missing_fields:
        raise ValueError(
            f"AI response is missing required fields: {sorted(missing_fields)}"
        )

    return result

if __name__ == "__main__":
    import sys
    test_output = sys.stdin.read()
    
    if not test_output.strip():
        print("No test output received.")
        sys.exit(1)

    try:
        result = analyze_failure(test_output)
        print(json.dumps(result, indent=2))
    except Exception as exc:
        print(f"AI agent failed: {exc}")
        sys.exit(1)
