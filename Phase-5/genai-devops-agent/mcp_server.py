from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "DevOps Knowledge Server"
)


@mcp.tool()
def search_docs(
    query: str
) -> str:

    knowledge_dir = Path(
        "knowledge"
    )

    matches = []

    if not knowledge_dir.exists():

        return "Knowledge directory not found."

    for file in knowledge_dir.glob(
        "*.md"
    ):

        content = file.read_text(
            encoding="utf-8"
        )

        if query.lower() in content.lower():

            matches.append(
                f"""
--- {file} ---

{content}
"""
            )

    if not matches:

        return (
            "No matching documentation found."
        )

    return "\n".join(matches)


@mcp.tool()
def list_docs() -> list[str]:

    knowledge_dir = Path(
        "knowledge"
    )

    if not knowledge_dir.exists():

        return []

    return [
        str(file)
        for file in knowledge_dir.glob(
            "*.md"
        )
    ]


if __name__ == "__main__":

    mcp.run()