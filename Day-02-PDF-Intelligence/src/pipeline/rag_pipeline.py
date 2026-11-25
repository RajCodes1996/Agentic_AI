from src.embeddings import EmbeddingService
from src.ingestion import TextChunker, chunk_text
from src.retrieval import Retriever, VectorStore
from src.pipeline.rag_answer_service import RAGAnswerService

class RAGPipeline:
    def __init__(
        self,
        llm,
        embedding_service=None,
        chunk_size=900,
        chunk_overlap=150,
        persist_directory="data/chroma_pdf_agent",
        collection_name="pdf_agent_documents"
    ):
        self.llm = llm
        self.embeddings = embedding_service or EmbeddingService()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        self.retriever = Retriever(self.embeddings, self.store)

    def _embed_documents(self, texts: list[str]) -> list[list[float]]:
        if hasattr(self.embeddings, "generate_embeddings"):
            embeddings = self.embeddings.generate_embeddings(texts)
        elif hasattr(self.embeddings, "generate_document_embeddings"):
            embeddings = self.embeddings.generate_document_embeddings(texts)
        elif hasattr(self.embeddings, "embed"):
            embeddings = self.embeddings.embed(texts)
        else:
            raise AttributeError(
                "Embedding service must implement "
                "'generate_embeddings', 'generate_document_embeddings', "
                "or 'embed'."
            )

        return [
            emb.tolist() if hasattr(emb, "tolist") else list(emb)
            for emb in embeddings
        ]

    def _embed_query(self, query: str) -> list[float]:
        if hasattr(self.embeddings, "generate_query_embedding"):
            emb = self.embeddings.generate_query_embedding(query)
        elif hasattr(self.embeddings, "embed"):
            emb = self.embeddings.embed([query])[0]
        else:
            raise AttributeError("Embedding service must implement 'generate_query_embedding' or 'embed'.")

        return emb.tolist() if hasattr(emb, "tolist") else list(emb)

    def index(self, text: str | list[dict], source_name: str = "document") -> int:
        if isinstance(text, list):
            chunker = TextChunker(self.chunk_size, self.chunk_overlap)
            raw_chunks = chunker.chunk_pages(text)
        else:
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
        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        self.store.add_chunks(chunks_for_store, embeddings)
        self.retriever = Retriever(self.embeddings, self.store)
        return len(chunks_for_store)

    from src.embeddings import EmbeddingService
from src.ingestion import TextChunker, chunk_text
from src.pipeline.rag_answer_service import RAGAnswerService
from src.retrieval import Retriever, VectorStore


class RAGPipeline:
    def __init__(
        self,
        llm,
        embedding_service=None,
        chunk_size=900,
        chunk_overlap=150,
        persist_directory="data/chroma_pdf_agent",
        collection_name="pdf_agent_documents"
    ):
        self.llm = llm
        self.embeddings = embedding_service or EmbeddingService()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        self.retriever = Retriever(self.embeddings, self.store)

    def _embed_documents(self, texts: list[str]) -> list[list[float]]:
        if hasattr(self.embeddings, "generate_embeddings"):
            embeddings = self.embeddings.generate_embeddings(texts)
        elif hasattr(self.embeddings, "generate_document_embeddings"):
            embeddings = self.embeddings.generate_document_embeddings(texts)
        elif hasattr(self.embeddings, "embed"):
            embeddings = self.embeddings.embed(texts)
        else:
            raise AttributeError(
                "Embedding service must implement "
                "'generate_embeddings', 'generate_document_embeddings', "
                "or 'embed'."
            )

        return [
            emb.tolist() if hasattr(emb, "tolist") else list(emb)
            for emb in embeddings
        ]

    def _embed_query(self, query: str) -> list[float]:
        if hasattr(self.embeddings, "generate_query_embedding"):
            emb = self.embeddings.generate_query_embedding(query)
        elif hasattr(self.embeddings, "embed"):
            emb = self.embeddings.embed([query])[0]
        else:
            raise AttributeError("Embedding service must implement 'generate_query_embedding' or 'embed'.")

        return emb.tolist() if hasattr(emb, "tolist") else list(emb)

    def index(self, text: str | list[dict], source_name: str = "document") -> int:
        if isinstance(text, list):
            chunker = TextChunker(self.chunk_size, self.chunk_overlap)
            raw_chunks = chunker.chunk_pages(text)
        else:
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
        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        self.store.add_chunks(chunks_for_store, embeddings)
        self.retriever = Retriever(self.embeddings, self.store)
        return len(chunks_for_store)

    def answer(self, question: str, k: int = 4) -> tuple[str, list[dict]]:
        """
        Retrieve relevant passages and generate a grounded answer.
        """
        answer_service = RAGAnswerService(
            retriever=self.retriever,
            llm_provider=self.llm
        )
        result = answer_service.answer(
            question=question,
            top_k=k
        )
        return result["answer"], result["sources"]