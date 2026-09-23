import os


# -----------------------------
# OpenAI Configuration
# -----------------------------

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6"
)


# -----------------------------
# Agent Configuration
# -----------------------------

MAX_AGENT_ITERATIONS = int(
    os.getenv(
        "MAX_AGENT_ITERATIONS",
        "12"
    )
)

MAX_REPAIR_ATTEMPTS = int(
    os.getenv(
        "MAX_REPAIR_ATTEMPTS",
        "3"
    )
)


# -----------------------------
# Repository Safety
# -----------------------------

ALLOWED_FILES = {
    "app.py",
}


PROTECTED_FILES = {
    "test_app.py",
    "requirements.txt",
    ".github/workflows/ai-devops.yml",
}


# -----------------------------
# Agent Behaviour
# -----------------------------

MIN_CONFIDENCE = 0.80