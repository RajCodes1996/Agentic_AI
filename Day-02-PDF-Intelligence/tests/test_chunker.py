
import pytest

from src.ingestion.chunker import TextChunker


def test_basic_chunking():

    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200
    )

    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunker.chunk_pages(pages)

    assert len(chunks) == 3

    assert chunks[0]["page_number"] == 1

    assert chunks[0]["chunk_id"] == 0

    assert len(chunks[0]["text"]) == 1000


def test_chunk_overlap():

    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200
    )

    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunker.chunk_pages(pages)

    # The first chunk ends at 1000.
    # The second chunk begins at 800.
    assert chunks[0]["text"][-200:] == \
           chunks[1]["text"][:200]


def test_page_number_preservation():

    chunker = TextChunker(
        chunk_size=1000,
        chunk_overlap=200
    )

    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        },
        {
            "page_number": 2,
            "text": "B" * 1500
        }
    ]

    chunks = chunker.chunk_pages(pages)

    page_numbers = [
        chunk["page_number"]
        for chunk in chunks
    ]

    assert page_numbers == [1, 1, 1, 2, 2]


def test_empty_pages():

    chunker = TextChunker()

    pages = [
        {
            "page_number": 1,
            "text": ""
        }
    ]

    chunks = chunker.chunk_pages(pages)

    assert chunks == []


def test_invalid_chunk_parameters():

    with pytest.raises(ValueError):
        TextChunker(chunk_size=0)

    with pytest.raises(ValueError):
        TextChunker(
            chunk_size=100,
            chunk_overlap=100
        )


def test_natural_boundary_splitting():

    chunker = TextChunker(
        chunk_size=100,
        chunk_overlap=20
    )

    pages = [
        {
            "page_number": 1,
            "text": (
                "Artificial intelligence is transforming "
                "modern industries. "
                "Machine learning enables computers to "
                "learn from data. "
                "Deep learning uses neural networks."
            )
        }
    ]

    chunks = chunker.chunk_pages(pages)

    assert len(chunks) > 1

    assert all(
        chunk["page_number"] == 1
        for chunk in chunks
    )

    assert all(
        chunk["text"].strip()
        for chunk in chunks
    )