from src.embeddings import EmbeddingService
from src.ingestion import chunk_text
from src.retrieval import Retriever, VectorStore

class RAGPipeline:
    def __init__(self, llm, embedding_service=None, chunk_size=900, chunk_overlap=150):
        self.llm = llm
        self.embeddings = embedding_service or EmbeddingService()
        self.chunk_size, self.chunk_overlap = chunk_size, chunk_overlap
        self.store = VectorStore()
        self.retriever = Retriever(self.store, self.embeddings)

    def index(self, text: str, source_name: str = "document") -> int:
        chunks = chunk_text(text, self.chunk_size, self.chunk_overlap)
        self.store = VectorStore()
        self.store.add(chunks, self.embeddings.embed(chunks), [{"source": source_name, "chunk": i + 1} for i in range(len(chunks))])
        self.retriever = Retriever(self.store, self.embeddings)
        return len(chunks)

    def answer(self, question: str, k: int = 4) -> tuple[str, list[dict]]:
        sources = self.retriever.retrieve(question, k)
        context = "\n\n".join(f"[Chunk {item['metadata']['chunk']}] {item['text']}" for item in sources)
        prompt = f"Answer only from the supplied context. If the answer is absent, say so. Cite chunk numbers.\n\nContext:\n{context}\n\nQuestion: {question}"
        return self.llm.generate(prompt), sources
