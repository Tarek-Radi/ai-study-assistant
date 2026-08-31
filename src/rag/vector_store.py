from typing import Any

import faiss
import numpy as np

from src.rag.embeddings import generate_embeddings

# convert Python list (List[list[float32]]) to Numpy array to deal with FAISS 
def build_faiss_index(
    embeddings: list[list[float]],
) -> faiss.IndexFlatIP:
    """Build a FAISS index from normalized embeddings."""

    embeddings_array = np.array(
        embeddings,
        dtype="float32",
    )

    dimension = embeddings_array.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings_array)

    return index


def search_faiss(
    query: str,
    index: faiss.IndexFlatIP,
    chunks: list[dict[str, Any]],
    top_k: int = 3,
    min_score: float = 0.4,
) -> list[dict[str, Any]]:
    """Search FAISS and return relevant chunks above a similarity threshold."""

    query_embedding = generate_embeddings([query])

    query_array = np.array(
        query_embedding,
        dtype="float32",
    )

    scores, indices = index.search(
        query_array,
        top_k,
    )

    results = []

    for score, chunk_index in zip(
        scores[0],
        indices[0],
    ):
        if chunk_index == -1:
            continue

        if score < min_score:
            continue

        chunk = chunks[chunk_index]

        results.append(
            {
                "score": float(score),
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "content": chunk["content"],
            }
        )

    return results


if __name__ == "__main__":
    from src.rag.chunker import chunk_documents
    from src.rag.document_loader import load_text_files

    documents = load_text_files()

    chunks = chunk_documents(documents)

    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    index = build_faiss_index(embeddings)

    query = "What is cosine similarity?"

    results = search_faiss(
        query=query,
        index=index,
        chunks=chunks,
        top_k=3,
        min_score=0.4,
    )

    print(f"Query: {query}")
    print(f"Results found: {len(results)}")

    if not results:
        print("No relevant chunks found.")

    for result in results:
        print("\n--------------------")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Chunk: {result['chunk_index']}")
        print(result["content"])