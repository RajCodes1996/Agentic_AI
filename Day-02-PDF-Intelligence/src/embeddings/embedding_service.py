"""Embedding adapter with a dependency-free lexical fallback."""
import math
import re
from collections import Counter

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(model_name)
        except Exception:
            pass

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self._model is not None:
            return self._model.encode(texts, normalize_embeddings=True).tolist()
        return [self._lexical_vector(text) for text in texts]

    @staticmethod
    def _lexical_vector(text: str, dimensions: int = 256) -> list[float]:
        counts = Counter(re.findall(r"\w+", text.lower()))
        values = [0.0] * dimensions
        for word, count in counts.items():
            values[hash(word) % dimensions] += count
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return [value / norm for value in values]
