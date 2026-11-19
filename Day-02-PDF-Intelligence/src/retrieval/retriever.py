from .vector_store import VectorStore

class Retriever:
    def __init__(self, store: VectorStore, embeddings):
        self.store, self.embeddings = store, embeddings

    def retrieve(self, query: str, k: int = 4) -> list[dict]:
        query_vector = self.embeddings.embed([query])[0]
        return [{"text": record.text, "score": score, "metadata": record.metadata} for record, score in self.store.search(query_vector, k)]
