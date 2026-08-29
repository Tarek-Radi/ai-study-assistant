from typing import Any

from src.rag.chunker import chunk_documents
from src.rag.document_loader import load_text_files
from src.rag.embeddings import generate_embeddings
from src.rag.vector_store import build_faiss_index, search_faiss


def build_retriever():
    """Build the knowledge base and return the FAISS index with its chunks."""

    documents = load_text_files()

    chunks = chunk_documents(documents)

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    index = build_faiss_index(embeddings)

    return index, chunks


def retrieve(
    query: str,
    index,
    chunks: list[dict[str, Any]],
    top_k: int = 3,
    min_score: float = 0.4,
) -> list[dict[str, Any]]:
    """Retrieve relevant chunks for a query."""

    return search_faiss(
        query=query,
        index=index,
        chunks=chunks,
        top_k=top_k,
        min_score=min_score,
    )


if __name__ == "__main__":
    index, chunks = build_retriever()

    query = "Why do we split documents into chunks?"

    results = retrieve(
        query=query,
        index=index,
        chunks=chunks,
    )

    print(f"Query: {query}")
    print(f"Results: {len(results)}")

    for result in results:
        print("\n--------------------")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Chunk: {result['chunk_index']}")
        print(result["content"])