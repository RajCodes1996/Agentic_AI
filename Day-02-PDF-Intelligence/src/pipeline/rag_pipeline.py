from src.embeddings import EmbeddingService
from src.ingestion import chunk_text
from src.retrieval import Retriever, VectorStore


class RAGPipeline:
    def __init__(self, llm, embedding_service=None, chunk_size=900, chunk_overlap=150):
        self.llm = llm
        self.embeddings = embedding_service or EmbeddingService()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.store = VectorStore()
        self.retriever = Retriever(self.embeddings, self.store)

    def _embed_documents(self, texts: list[str]) -> list[list[float]]:
        if hasattr(self.embeddings, "generate_document_embeddings"):
            embeddings = self.embeddings.generate_document_embeddings(texts)
        elif hasattr(self.embeddings, "embed"):
            embeddings = self.embeddings.embed(texts)
        else:
            raise AttributeError("Embedding service must implement 'embed' or 'generate_document_embeddings'.")

        return [emb.tolist() if hasattr(emb, "tolist") else list(emb) for emb in embeddings]

    def _embed_query(self, query: str) -> list[float]:
        if hasattr(self.embeddings, "generate_query_embedding"):
            emb = self.embeddings.generate_query_embedding(query)
        elif hasattr(self.embeddings, "embed"):
            emb = self.embeddings.embed([query])[0]
        else:
            raise AttributeError("Embedding service must implement 'generate_query_embedding' or 'embed'.")

        return emb.tolist() if hasattr(emb, "tolist") else list(emb)

    def index(self, text: str, source_name: str = "document") -> int:
        raw_chunks = chunk_text(text, self.chunk_size, self.chunk_overlap)
        if not raw_chunks:
            return 0

        if isinstance(raw_chunks[0], dict):
            chunks_for_store = [
                {
                    **c,
                    "text": c["text"],
                    "page_number": c.get("page_number", 1),
                    "chunk_id": c.get("chunk_id", idx),
                    "source": c.get("source", source_name),
                    "chunk": idx + 1,
                }
                for idx, c in enumerate(raw_chunks)
            ]
            chunk_texts = [c["text"] for c in chunks_for_store]
        else:
            chunks_for_store = [
                {
                    "text": chunk_str,
                    "page_number": 1,
                    "chunk_id": idx,
                    "source": source_name,
                    "chunk": idx + 1,
                }
                for idx, chunk_str in enumerate(raw_chunks)
            ]
            chunk_texts = [c["text"] for c in chunks_for_store]

        embeddings = self._embed_documents(chunk_texts)
        self.store = VectorStore()
        self.store.add_chunks(chunks_for_store, embeddings)
        self.retriever = Retriever(self.embeddings, self.store)
        return len(chunks_for_store)

    def answer(self, question: str, k: int = 4) -> tuple[str, list[dict]]:
        if hasattr(self.retriever, "search"):
            try:
                sources = self.retriever.search(question, top_k=k)
            except AttributeError:
                query_vec = self._embed_query(question)
                total = self.store.collection.count()
                if total == 0:
                    sources = []
                else:
                    res = self.store.collection.query(
                        query_embeddings=[query_vec],
                        n_results=min(k, total),
                        include=["documents", "metadatas", "distances"],
                    )
                    sources = [
                        {
                            "id": cid,
                            "text": doc,
                            "page_number": meta.get("page_number", 1),
                            "chunk_id": meta.get("chunk_id", idx),
                            "metadata": meta,
                            "distance": float(dist),
                        }
                        for idx, (cid, doc, meta, dist) in enumerate(
                            zip(
                                res["ids"][0],
                                res["documents"][0],
                                res["metadatas"][0],
                                res["distances"][0],
                            )
                        )
                    ]
        else:
            sources = self.retriever.retrieve(question, k)

        context_blocks = []
        for idx, item in enumerate(sources, start=1):
            meta = item.get("metadata") or {}
            chunk_num = meta.get("chunk", item.get("chunk_id", idx))
            context_blocks.append(f"[Chunk {chunk_num}] {item['text']}")

        context = "\n\n".join(context_blocks)
        prompt = (
            "Answer only from the supplied context. If the answer is absent, say so. "
            f"Cite chunk numbers.\n\nContext:\n{context}\n\nQuestion: {question}"
        )
        return self.llm.generate(prompt), sources