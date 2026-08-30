from pathlib import Path

from pypdf import PdfReader


KNOWLEDGE_DIR = Path("data/knowledge")

PDF_DIR = KNOWLEDGE_DIR / "pdf"
TXT_DIR = KNOWLEDGE_DIR / "txt"


def validate_content(
    content: str,
    source: str,
) -> str:
    """Validate extracted document content."""

    cleaned_content = content.strip()

    if not cleaned_content:
        raise ValueError(
            f"Document '{source}' is empty or contains no readable text."
        )

    return cleaned_content


def load_text_file(
    file_path: Path,
) -> dict[str, str]:
    """Load and validate a TXT document."""

    content = file_path.read_text(
        encoding="utf-8",
    )

    content = validate_content(
        content=content,
        source=file_path.name,
    )

    return {
        "source": file_path.name,
        "type": "txt",
        "content": content,
    }


def load_pdf_file(
    file_path: Path,
) -> dict[str, str]:
    """Extract and validate text from a PDF document."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text)

    content = "\n".join(pages)

    content = validate_content(
        content=content,
        source=file_path.name,
    )

    return {
        "source": file_path.name,
        "type": "pdf",
        "content": content,
    }


def load_documents(
    source_type: str,
) -> list[dict[str, str]]:
    """Load documents from the selected knowledge source."""

    documents = []

    source_type = source_type.lower().strip()

    if source_type == "pdf":
        source_dir = PDF_DIR
        pattern = "*.pdf"
        loader = load_pdf_file

    elif source_type == "txt":
        source_dir = TXT_DIR
        pattern = "*.txt"
        loader = load_text_file

    else:
        raise ValueError(
            "source_type must be either 'pdf' or 'txt'."
        )

    if not source_dir.exists():
        return documents

    for file_path in source_dir.glob(pattern):
        if not file_path.is_file():
            continue

        document = loader(file_path)

        documents.append(document)

    return documents


if __name__ == "__main__":

    source_type = "pdf"

    documents = load_documents(
        source_type=source_type,
    )

    print(
        f"Source type: {source_type}"
    )

    print(
        f"Documents loaded: {len(documents)}"
    )

    if not documents:
        print(
            "No documents found."
        )

    for document in documents:
        print("\n--------------------")
        print(
            f"Source: {document['source']}"
        )
        print(
            f"Type: {document['type']}"
        )
        print(
            f"Characters: "
            f"{len(document['content'])}"
        )
        print(
            document["content"][:300]
        )