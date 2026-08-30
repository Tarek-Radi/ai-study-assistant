from typing import Any

from src.rag.chunker import chunk_documents
from src.rag.document_loader import load_documents
from src.rag.embeddings import generate_embeddings
from src.rag.vector_store import (
    build_faiss_index,
    search_faiss,
)


def build_retriever(
    source_type: str = "pdf", ########## Choice pdf or txt #####################
):
    """Build the knowledge base retriever for the selected source type."""

    documents = load_documents(
        source_type=source_type,
    )

    if not documents:
        raise ValueError(
            f"No valid {source_type.upper()} documents "
            f"were found in the knowledge base."
        )

    chunks = chunk_documents(
        documents
    )

    if not chunks:
        raise ValueError(
            "No chunks were generated from the knowledge base."
        )

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    index = build_faiss_index(
        embeddings
    )

    return index, chunks


def retrieve(
    query: str,
    index,
    chunks: list[dict[str, Any]],
    top_k: int = 3,
    min_score: float = 0.4,
) -> list[dict[str, Any]]:
    """Retrieve relevant chunks for a query."""

    cleaned_query = query.strip()

    if not cleaned_query:
        raise ValueError(
            "Query cannot be empty."
        )

    return search_faiss(
        query=cleaned_query,
        index=index,
        chunks=chunks,
        top_k=top_k,
        min_score=min_score,
    )


if __name__ == "__main__":

    source_type = "pdf"   ### To test 

    try:
        index, chunks = build_retriever(
            source_type=source_type,
        )

        query = (
            "What is the difference between functional "
            "and non-functional requirements?"
        )
        # query = "How does a turbojet engine generate thrust?"
        #To test txt
        # query = (
        #     "what is rag?"
        # )

        results = retrieve(
            query=query,
            index=index,
            chunks=chunks,
            top_k=3,
            min_score=0.4,
        )

        print(
            f"Source type: {source_type}"
        )

        print(
            f"Query: {query}"
        )

        print(
            f"Results: {len(results)}"
        )

        if not results:
            print(
                "No relevant chunks found."
            )

        for result in results:

            print(
                "\n--------------------"
            )

            print(
                f"Score: "
                f"{result['score']:.4f}"
            )

            print(
                f"Source: "
                f"{result['source']}"
            )

            print(
                f"Chunk: "
                f"{result['chunk_index']}"
            )

            print(
                result["content"]
            )

    except ValueError as error:
        print(
            f"Retriever error: {error}"
        )