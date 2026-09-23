# GenAI analyzer

import os
import sys
from openai import OpenAI

def analyze_failure(error_log):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a DevOps CI/CD troubleshooting assistant.

A GitHub Actions pipeline has failed.

Analyze the following test failure:

---------------- ERROR LOG ----------------

{error_log}

--------------------------------------------

Provide your response in this format:

1. Root Cause
2. Failed Test
3. Likely Problem
4. Recommended Fix
5. Corrected Code
6. Prevention Recommendation

Be concise and technically accurate.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text

if __name__ == "__main__":
    error_log = sys.stdin.read()

    if not error_log.strip():
        print("No error log received.")
        sys.exit(1)

    try:
        result = analyze_failure(error_log)
        print(result)
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)
