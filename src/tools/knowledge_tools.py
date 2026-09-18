from typing import Any

from src.rag.retriever import (
    build_retriever,
    retrieve,
)


PDF_INDEX, PDF_CHUNKS = build_retriever(
    source_type="pdf",
)


def search_knowledge_base(
    query: str,
    top_k: int = 3,
) -> dict[str, Any]:
    """Search the PDF knowledge base for relevant study content."""

    results = retrieve(
        query=query,
        index=PDF_INDEX,
        chunks=PDF_CHUNKS,
        top_k=top_k,
        min_score=0.4,
    )

    return {
        "query": query,
        "count": len(results),
        "results": results,
    }