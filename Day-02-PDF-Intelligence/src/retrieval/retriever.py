
class Retriever:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Retrieve the most relevant document chunks for a query."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query cannot be empty.")

        if (
            not isinstance(top_k, int)
            or isinstance(top_k, bool)
            or top_k <= 0
        ):
            raise ValueError("top_k must be a positive integer.")

        collection = self.vector_store.collection
        total_chunks = collection.count()

        if total_chunks == 0:
            return []

        query_embedding = self.embedding_service.generate_query_embedding(
            query.strip()
        )

        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, total_chunks),
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for chunk_id, document, metadata, distance in zip(
            ids, documents, metadatas, distances
        ):
            retrieved_chunks.append({
                "id": chunk_id,
                "text": document,
                "page_number": metadata["page_number"],
                "chunk_id": metadata["chunk_id"],
                "distance": float(distance)
            })

        return retrieved_chunks