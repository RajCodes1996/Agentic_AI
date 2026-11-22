
import numpy as np
import pytest

from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import VectorStore

class FakeEmbeddingService:
    def generate_query_embedding(self, query):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        return np.array([1.0, 0.0, 0.0], dtype=np.float32)

@pytest.fixture
def retriever(tmp_path):
    vector_store = VectorStore(
        persist_directory=str(tmp_path / "chroma_db"),
        collection_name="retriever_test"
    )

    chunks = [
        {
            "chunk_id": 0,
            "page_number": 1,
            "text": "Python is a programming language."
        },
        {
            "chunk_id": 1,
            "page_number": 2,
            "text": "Machine learning uses data to learn patterns."
        },
        {
            "chunk_id": 2,
            "page_number": 3,
            "text": "ChromaDB stores vector embeddings."
        }
    ]

    embeddings = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)

    vector_store.add_chunks(chunks, embeddings)

    return Retriever(
        embedding_service=FakeEmbeddingService(),
        vector_store=vector_store
    )

def test_retrieve_relevant_chunk(retriever):
    results = retriever.search("Tell me about Python")

    assert len(results) == 3
    assert results[0]["text"] == "Python is a programming language."
    assert results[0]["page_number"] == 1

def test_top_k_limit(retriever):
    results = retriever.search("Python", top_k=2)

    assert len(results) == 2

def test_top_k_larger_than_collection(retriever):
    results = retriever.search("Python", top_k=10)

    assert len(results) == 3

def test_empty_query(retriever):
    with pytest.raises(ValueError):
        retriever.search("")

def test_invalid_top_k(retriever):
    with pytest.raises(ValueError):
        retriever.search("Python", top_k=0)

def test_empty_collection(tmp_path):
    vector_store = VectorStore(
        persist_directory=str(tmp_path / "empty_db"),
        collection_name="empty_test"
    )

    retriever = Retriever(
        embedding_service=FakeEmbeddingService(),
        vector_store=vector_store
    )

    results = retriever.search("Python")

    assert results == []