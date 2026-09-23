# CI/CD Troubleshooting Guide

## Test Failure

When a test fails:

1. Read the complete error message.
2. Identify the failed test.
3. Read the corresponding application code.
4. Compare expected and actual behavior.
5. Make the smallest application-code change.
6. Run the tests again.
7. Inspect git diff.

## Important Rule

Do not modify tests to make a failing application pass.

The application should be corrected instead.

## Deployment Troubleshooting

When deployment fails:

1. Check application logs.
2. Check environment variables.
3. Check Python version.
4. Check dependency versions.
5. Check container logs.
6. Check health checks.