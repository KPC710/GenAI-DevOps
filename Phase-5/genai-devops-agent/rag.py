from pathlib import Path


KNOWLEDGE_DIRECTORY = Path("knowledge")


def load_documents():

    documents = []

    if not KNOWLEDGE_DIRECTORY.exists():
        return documents

    for file in KNOWLEDGE_DIRECTORY.glob("*.md"):

        content = file.read_text(
            encoding="utf-8"
        )

        documents.append({
            "file": str(file),
            "content": content
        })

    return documents


def search_knowledge(query: str):

    documents = load_documents()

    query_words = set(
        query.lower().split()
    )

    results = []

    for document in documents:

        words = set(
            document["content"]
            .lower()
            .split()
        )

        score = len(
            query_words.intersection(words)
        )

        if score > 0:

            results.append({
                "file": document["file"],
                "score": score,
                "content": document["content"]
            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:3]
