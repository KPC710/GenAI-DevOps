import os
import subprocess
import json


# --------------------------------------------------
# Execute GitHub CLI
# --------------------------------------------------

def run_gh(args):

    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        return {
            "success": False,
            "error": result.stderr
        }

    return {
        "success": True,
        "output": result.stdout
    }


# --------------------------------------------------
# Repository
# --------------------------------------------------

def get_repository():

    repository = os.getenv(
        "GITHUB_REPOSITORY"
    )

    if not repository:

        return {
            "success": False,
            "error": "GITHUB_REPOSITORY is not configured."
        }

    return {
        "success": True,
        "repository": repository
    }


# --------------------------------------------------
# Workflow runs
# --------------------------------------------------

def get_workflow_runs():

    result = run_gh([
        "run",
        "list",
        "--limit",
        "10",
        "--json",
        "databaseId,name,status,conclusion,headBranch,createdAt"
    ])

    if not result["success"]:
        return result

    try:

        return {
            "success": True,
            "runs": json.loads(
                result["output"]
            )
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "error": "Unable to parse GitHub response."
        }


# --------------------------------------------------
# Pull requests
# --------------------------------------------------

def get_pull_requests():

    result = run_gh([
        "pr",
        "list",
        "--limit",
        "10",
        "--json",
        "number,title,state,headRefName,baseRefName,url"
    ])

    if not result["success"]:
        return result

    try:

        return {
            "success": True,
            "pull_requests": json.loads(
                result["output"]
            )
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "error": "Unable to parse PR response."
        }


# --------------------------------------------------
# PR details
# --------------------------------------------------

def get_pr_details(pr_number: int):

    result = run_gh([
        "pr",
        "view",
        str(pr_number),
        "--json",
        "number,title,state,body,author,commits,files,url"
    ])

    return result


# --------------------------------------------------
# Create branch
# --------------------------------------------------

def create_branch(branch_name):

    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        return {
            "success": False,
            "error": result.stderr
        }

    sha = result.stdout.strip()

    return run_gh([
        "api",
        f"repos/{os.environ['GITHUB_REPOSITORY']}/git/refs",
        "-f",
        f"ref=refs/heads/{branch_name}",
        "-f",
        f"sha={sha}"
    ])


# --------------------------------------------------
# Push branch
# --------------------------------------------------

def push_branch(branch_name):

    result = subprocess.run(
        [
            "git",
            "push",
            "origin",
            branch_name
        ],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


# --------------------------------------------------
# Create pull request
# --------------------------------------------------

def create_pull_request(
    branch_name,
    title,
    body
):

    return run_gh([
        "pr",
        "create",
        "--head",
        branch_name,
        "--base",
        "main",
        "--title",
        title,
        "--body",
        body
    ])
