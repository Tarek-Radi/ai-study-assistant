from typing import Any

import src
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

    if not results:
        return {
            "query": query,
            "count": 0,
            "message": (
                "No relevant information was found "
                "in the study material."
            ),
            "results": [],
        }

    return {
        "query": query,
        "count": len(results),
        "results": results,
    }
    
SEARCH_KNOWLEDGE_BASE_TOOL = {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": (
            "Search the user's uploaded study materials and knowledge base. "
            "You MUST use this tool whenever the user asks about their "
            "study material, uploaded documents, PDFs, notes, knowledge base, "
            "or says 'according to my study material'. "
            "Do not answer those questions from general model knowledge."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's question to search for.",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Maximum number of relevant chunks to return.",
                    "default": 3,
                },
            },
            "required": ["query"],
        },
    },
}