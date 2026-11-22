
import numpy as np
import pytest

from src.retrieval.vector_store import VectorStore

@pytest.fixture
def vector_store(tmp_path):

    return VectorStore(
        persist_directory=str(tmp_path / "chroma_db"),
        collection_name="test_documents"
    )

@pytest.fixture
def sample_chunks():

    return [
        {
            "chunk_id": 0,
            "page_number": 1,
            "text": "Artificial intelligence is transforming industries."
        },
        {
            "chunk_id": 1,
            "page_number": 2,
            "text": "Machine learning is a subset of artificial intelligence."
        }
    ]

@pytest.fixture
def sample_embeddings():

    return np.array(
        [
            [0.8, 0.2, 0.1],
            [0.7, 0.3, 0.2]
        ],
        dtype=np.float32
    )

def test_store_chunks(
    vector_store,
    sample_chunks,
    sample_embeddings
):

    count = vector_store.add_chunks(
        sample_chunks,
        sample_embeddings
    )

    assert count == 2

    assert vector_store.get_collection_count() == 2

def test_store_metadata(
    vector_store,
    sample_chunks,
    sample_embeddings
):

    vector_store.add_chunks(
        sample_chunks,
        sample_embeddings
    )

    result = vector_store.collection.get(
        ids=["chunk_0"]
    )

    assert result["metadatas"][0]["page_number"] == 1

    assert result["metadatas"][0]["chunk_id"] == 0

def test_empty_chunks(vector_store):

    result = vector_store.add_chunks(
        [],
        np.empty((0, 3))
    )

    assert result == 0

def test_mismatched_embeddings(vector_store):

    chunks = [
        {
            "chunk_id": 0,
            "page_number": 1,
            "text": "Sample document."
        }
    ]

    embeddings = np.empty((0, 3))

    with pytest.raises(ValueError):
        vector_store.add_chunks(chunks, embeddings)

def test_duplicate_chunk_ids(vector_store):

    chunks = [
        {
            "chunk_id": 0,
            "page_number": 1,
            "text": "First chunk."
        },
        {
            "chunk_id": 0,
            "page_number": 2,
            "text": "Second chunk."
        }
    ]

    embeddings = np.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
    )

    with pytest.raises(ValueError):
        vector_store.add_chunks(chunks, embeddings)

def test_persistence(
    tmp_path,
    sample_chunks,
    sample_embeddings
):

    db_path = str(tmp_path / "persistent_db")

    first_store = VectorStore(
        persist_directory=db_path,
        collection_name="persistence_test"
    )

    first_store.add_chunks(
        sample_chunks,
        sample_embeddings
    )

    second_store = VectorStore(
        persist_directory=db_path,
        collection_name="persistence_test"
    )

    assert second_store.get_collection_count() == 2