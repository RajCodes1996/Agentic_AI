from src.embeddings.embedding_service import EmbeddingService

def test_embed_returns_one_vector_per_text():
    vectors = EmbeddingService().embed(["alpha beta", "beta gamma"])
    assert len(vectors) == 2
    assert len(vectors[0]) == len(vectors[1])
