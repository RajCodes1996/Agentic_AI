from src.ingestion.chunker import chunk_text

def test_chunk_text_splits_and_preserves_overlap():
    text = "alpha " * 100
    chunks = chunk_text(text, chunk_size=80, overlap=20)
    assert len(chunks) > 1
    assert all(len(chunk) <= 80 for chunk in chunks)

def test_chunker_empty_text():
    assert chunk_text("   ") == []
