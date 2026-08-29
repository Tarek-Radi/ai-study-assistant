from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(MODEL_NAME)

    return _embedding_model


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """Generate normalized embeddings for a list of texts."""

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


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

    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Vector dimension: {len(embeddings[0])}")
    print(f"First vector sample: {embeddings[0][:10]}")