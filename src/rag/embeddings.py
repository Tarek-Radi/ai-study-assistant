from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model() -> SentenceTransformer:
    """Load and return the embedding model."""

    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """Generate embeddings for a list of texts."""

    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


if __name__ == "__main__":
    from src.rag.document_loader import load_text_files
    from src.rag.chunker import chunk_documents

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