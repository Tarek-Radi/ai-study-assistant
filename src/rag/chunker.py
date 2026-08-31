import re
from typing import Any


def split_sentences(text: str) -> list[str]:
    """Split text into sentences."""

    sentences = re.split(r"(?<=[.!?؟])\s+", text.strip()) #######****Important***##############<========

    return [
        sentence.strip()                # VALUE = result.append(sentence.strip()) appended there
        for sentence in sentences       # for item in items
        if sentence.strip()             # if CONDITION
        #================================================= Exact Equal 
        # cleaned_sentences = []
        # for sentence in sentences:
        #     if sentence.strip():
        #         cleaned_sentences.append(
        #             sentence.strip()
        #         )
        # return cleaned_sentences
    ]


def chunk_text(
    text: str,
    chunk_size: int = 500,    #############
    overlap_sentences: int = 1,
) -> list[str]:
    """Split text into sentence-aware overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap_sentences < 0:
        raise ValueError("overlap_sentences cannot be negative.")

    sentences = split_sentences(text)

    chunks = []
    current_sentences = []

    for sentence in sentences:
        candidate = " ".join(current_sentences + [sentence])

        if len(candidate) <= chunk_size:
            current_sentences.append(sentence)

        else:
            if current_sentences:
                chunks.append(" ".join(current_sentences))

                if overlap_sentences > 0:
                    current_sentences = current_sentences[-overlap_sentences:]
                else:
                    current_sentences = []

            # Very long sentence fallback
            if len(sentence) > chunk_size:
                words = sentence.split()
                temporary_chunk = ""

                for word in words:
                    candidate = f"{temporary_chunk} {word}".strip()

                    if len(candidate) <= chunk_size:
                        temporary_chunk = candidate
                    else:
                        if temporary_chunk:
                            chunks.append(temporary_chunk)

                        temporary_chunk = word

                current_sentences = (
                    [temporary_chunk]
                    if temporary_chunk
                    else []
                )

            else:
                candidate = " ".join(current_sentences + [sentence])

                # Avoid overlap causing chunk_size overflow
                if len(candidate) > chunk_size:
                    current_sentences = [sentence]
                else:
                    current_sentences.append(sentence)

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks


def chunk_documents(
    documents: list[dict[str, str]],
    chunk_size: int = 500,
    overlap_sentences: int = 1,
) -> list[dict[str, Any]]:
    """Split documents into chunks while preserving metadata."""

    all_chunks = []

    for document in documents:
        chunks = chunk_text(
            document["content"],
            chunk_size=chunk_size,
            overlap_sentences=overlap_sentences,
        )

        for index, content in enumerate(chunks):
            all_chunks.append(
                {
                    "source": document["source"],
                    "chunk_index": index,
                    "content": content,
                }
            )

    return all_chunks


if __name__ == "__main__":
    from src.rag.document_loader import load_text_files

    documents = load_text_files()

    chunks = chunk_documents(
        documents,
        chunk_size=500,
        overlap_sentences=1,
    )

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    for chunk in chunks[:9]:
        print("\n--------------------")
        print(f"Source: {chunk['source']}")
        print(f"Chunk: {chunk['chunk_index']}")
        print(f"Characters: {len(chunk['content'])}")
        print(chunk["content"])