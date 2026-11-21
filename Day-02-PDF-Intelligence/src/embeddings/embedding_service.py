
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        model=None
    ):

        """
        Initialize the embedding model.

        An optional model argument allows us to inject
        a mock model during automated testing.
        """

        if model is not None:
            self.model = model
        else:
            self.model = SentenceTransformer(model_name)

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> np.ndarray:

        """
        Convert multiple text passages into embeddings.
        """

        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        if any(
            not isinstance(text, str) or not text.strip()
            for text in texts
        ):
            raise ValueError(
                "All input texts must be non-empty strings."
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return np.asarray(embeddings, dtype=np.float32)

    def generate_query_embedding(
        self,
        query: str
    ) -> np.ndarray:

        """
        Convert a user question into an embedding.
        """

        if not isinstance(query, str) or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return np.asarray(embedding, dtype=np.float32)
