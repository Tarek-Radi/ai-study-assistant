from pathlib import Path


KNOWLEDGE_DIR = Path("data/knowledge")


def load_text_files() -> list[dict[str, str]]:
    """Load all TXT files from the knowledge directory."""

    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents


if __name__ == "__main__":
    documents = load_text_files()

    for document in documents:
        print(f"\nSource: {document['source']}")
        print(f"Characters: {len(document['content'])}")
        print(document["content"][:200])