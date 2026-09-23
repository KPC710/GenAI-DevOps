# Deployment Guidelines

## Before Deployment

Always:

1. Run pytest.
2. Confirm all tests pass.
3. Build the Docker image.
4. Verify required environment variables.
5. Check application health.

## Production

Production uses Python 3.12.

## Safety

Never deploy an application when the test suite is failing.

## Docker

Check Docker logs when the application fails after deployment.

## Environment Variables

Never hard-code secrets into source code.

Use environment variables or a secure secret manager.