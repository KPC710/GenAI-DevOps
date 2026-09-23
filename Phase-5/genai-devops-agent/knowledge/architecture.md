<!-- Instead of relying only on what the LLM learned during training, we'll give it your organization's documentation. -->

# Application Architecture

# DevOps Agent Architecture

## Application

app.py contains the application business logic.

## Tests

test_app.py contains unit tests for the application.

## CI/CD

.github/workflows/ai-devops.yml contains the GitHub Actions pipeline.

## AI Agent

agent.py is responsible for analyzing failures and coordinating tools.

## Tools

tools.py provides safe repository operations.

## GitHub

github_tools.py provides GitHub related operations.

## Knowledge

The knowledge directory contains internal DevOps documentation.