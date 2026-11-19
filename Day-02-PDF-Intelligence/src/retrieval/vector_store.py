"""Small in-memory vector store designed for a single uploaded document."""
from dataclasses import dataclass
import math

@dataclass
class VectorRecord:
    text: str
    embedding: list[float]
    metadata: dict

class VectorStore:
    def __init__(self):
        self.records: list[VectorRecord] = []

    def add(self, texts: list[str], embeddings: list[list[float]], metadatas: list[dict] | None = None) -> None:
        if len(texts) != len(embeddings):
            raise ValueError("texts and embeddings must have the same length")
        metadatas = metadatas or [{} for _ in texts]
        self.records.extend(VectorRecord(text, embedding, metadata) for text, embedding, metadata in zip(texts, embeddings, metadatas))

    def search(self, query_embedding: list[float], k: int = 4) -> list[tuple[VectorRecord, float]]:
        def score(record: VectorRecord) -> float:
            size = min(len(record.embedding), len(query_embedding))
            return sum(record.embedding[i] * query_embedding[i] for i in range(size)) if size else 0.0
        return sorted(((record, score(record)) for record in self.records), key=lambda item: item[1], reverse=True)[:k]
