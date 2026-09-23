import json
import os
import sys
from openai import OpenAI
from pathlib import Path

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

def read_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")

def build_prompt(test_output, source_code, test_code):
    prompt = f"""
You are an expert DevOps debugging agent.

A CI pipeline has failed.

Your job is to analyze the failure and propose a SAFE minimal code fix.

TEST OUTPUT
-----------
{test_output}

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
    client = OpenAI()
    source_code = read_file("Phase-3/genai-devops-demo/app.py")
    test_code = read_file("Phase-3/genai-devops-demo/test_app.py")
    prompt = build_prompt(test_output, source_code, test_code)

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a reliable software engineering agent. "
            "Return valid JSON only."
        ),
        input=prompt,
    )

    text = response.output_text.strip()

    # Handle accidental markdown fences.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

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
