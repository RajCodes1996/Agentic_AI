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
        collection_name="pdf_agent_documents",
    ):
        self.llm = llm
        self.embeddings = embedding_service or EmbeddingService()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Preserve original document pages for document-level questions.
        self.document_pages: list[dict] = []

        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
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

    def index(self, text: str | list[dict], source_name: str = "document") -> int:
        if isinstance(text, list):
            self.document_pages = [
                {
                    "page_number": page.get("page_number", index + 1),
                    "text": page.get("text", ""),
                }
                for index, page in enumerate(text)
                if page.get("text", "").strip()
            ]

            chunker = TextChunker(self.chunk_size, self.chunk_overlap)
            raw_chunks = chunker.chunk_pages(text)
        else:
            self.document_pages = (
                [{"page_number": 1, "text": text}] if text.strip() else []
            )

            raw_chunks = chunk_text(
                text,
                self.chunk_size,
                self.chunk_overlap,
            )

        if not raw_chunks:
            return 0

        if isinstance(raw_chunks[0], dict):
            chunks_for_store = [
                {
                    **chunk,
                    "text": chunk["text"],
                    "page_number": chunk.get("page_number", 1),
                    "chunk_id": chunk.get("chunk_id", index),
                    "source": chunk.get("source", source_name),
                    "chunk": index + 1,
                }
                for index, chunk in enumerate(raw_chunks)
            ]
        else:
            chunks_for_store = [
                {
                    "text": chunk_text_value,
                    "page_number": 1,
                    "chunk_id": index,
                    "source": source_name,
                    "chunk": index + 1,
                }
                for index, chunk_text_value in enumerate(raw_chunks)
            ]

        chunk_texts = [chunk["text"] for chunk in chunks_for_store]
        embeddings = self._embed_documents(chunk_texts)

        self.store = VectorStore(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )

        self.store.add_chunks(chunks_for_store, embeddings)
        self.retriever = Retriever(self.embeddings, self.store)

        return len(chunks_for_store)

    def answer(self, question: str, k: int = 4) -> tuple[str, list[dict]]:
        answer_service = RAGAnswerService(
            retriever=self.retriever,
            llm_provider=self.llm,
        )

        result = answer_service.answer(
            question=question,
            top_k=k,
            document_pages=self.document_pages,
        )

        return result["answer"], result["sources"]