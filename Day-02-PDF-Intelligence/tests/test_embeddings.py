
import numpy as np
import pytest

from src.embeddings.embedding_service import EmbeddingService


class FakeEmbeddingModel:

    def encode(self, texts, **kwargs):

        if isinstance(texts, str):
            return np.array(
                [1.0, 0.0, 0.0],
                dtype=np.float32
            )

        return np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0]
            ],
            dtype=np.float32
        )


def create_embedding_service():

    return EmbeddingService(
        model=FakeEmbeddingModel()
    )


def test_generate_embeddings():

    service = create_embedding_service()

    texts = [
        "Artificial intelligence is growing.",
        "Machine learning is a branch of AI."
    ]

    embeddings = service.generate_embeddings(texts)

    assert embeddings.shape == (2, 3)

    assert isinstance(embeddings, np.ndarray)

    assert embeddings.dtype == np.float32


def test_generate_query_embedding():

    service = create_embedding_service()

    embedding = service.generate_query_embedding(
        "What is artificial intelligence?"
    )

    assert embedding.shape == (3,)

    assert isinstance(embedding, np.ndarray)


def test_empty_text_list():

    service = create_embedding_service()

    embeddings = service.generate_embeddings([])

    assert embeddings.shape == (0, 384)


def test_invalid_document_text():

    service = create_embedding_service()

    with pytest.raises(ValueError):
        service.generate_embeddings(
            ["Valid text", ""]
        )


def test_empty_query():

    service = create_embedding_service()

    with pytest.raises(ValueError):
        service.generate_query_embedding("")


def test_embeddings_are_normalized():

    service = create_embedding_service()

    embeddings = service.generate_embeddings(
        ["First document", "Second document"]
    )

    norms = np.linalg.norm(embeddings, axis=1)

    assert np.allclose(norms, 1.0)
