
from pathlib import Path
import chromadb
import math

class VectorStore:

    def __init__(
        self,
        persist_directory: str = "data/chroma_db",
        collection_name: str = "pdf_documents"
    ):

        """
        Initialize a persistent ChromaDB vector store.
        """

        self.persist_directory = Path(persist_directory)

        # Create storage directory if necessary.
        self.persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # Initialize persistent ChromaDB client.
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        # Create or retrieve the collection.
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings
    ) -> int:

        """
        Store document chunks, embeddings and metadata.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        if not chunks:
            return 0

        ids = []
        documents = []
        metadatas = []
        vectors = []

        for chunk, embedding in zip(chunks, embeddings):

            text = chunk["text"]

            if not isinstance(text, str) or not text.strip():
                raise ValueError(
                    "Chunk text cannot be empty."
                )

            page_number = chunk["page_number"]
            chunk_id = chunk["chunk_id"]

            if (
                not isinstance(page_number, int)
                or isinstance(page_number, bool)
                or page_number < 1
            ):
                raise ValueError("Invalid page number.")

            if (
                not isinstance(chunk_id, int)
                or isinstance(chunk_id, bool)
                or chunk_id < 0
            ):
                raise ValueError("Invalid chunk ID.")

            vector = [float(value) for value in embedding]

            if not vector or any(
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                for value in vector
            ):
                raise ValueError("Invalid embedding vector.")

            if not all(math.isfinite(value) for value in vector):
                raise ValueError("Embedding contains non-finite values.")
            
            ids.append(f"chunk_{chunk_id}")
            documents.append(text)

            metadatas.append({
                "page_number": page_number,
                "chunk_id": chunk_id
            })

            vectors.append(vector)

        if len(set(ids)) != len(ids):
            raise ValueError(
                "Duplicate chunk IDs found in input."
            )

        # Upsert inserts new chunks or updates existing IDs.
        self.collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
        )

        return len(chunks)

    def get_collection_count(self) -> int:

        """
        Return the number of stored chunks.
        """

        return self.collection.count()