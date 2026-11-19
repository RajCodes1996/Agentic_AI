"""Deterministic, overlap-aware text chunking."""
def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap smaller than chunk_size")
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks, start = [], 0
    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        if end < len(clean):
            split = clean.rfind(" ", start, end)
            if split > start:
                end = split
        chunks.append(clean[start:end].strip())
        if end == len(clean):
            break
        start = max(end - overlap, start + 1)
    return chunks
