
class TextChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):

        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive.")

        if chunk_overlap < 0:
            raise ValueError("Chunk overlap cannot be negative.")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _find_boundary(self, text, start, end):

        """
        Find a natural text boundary near the end of a chunk.
        Avoid cutting sentences or words unnecessarily.
        """

        minimum_position = start + int(
            self.chunk_size * 0.8
        )

        boundaries = [
            text.rfind("\n\n", minimum_position, end),
            text.rfind("\n", minimum_position, end),
            text.rfind(". ", minimum_position, end),
            text.rfind("? ", minimum_position, end),
            text.rfind("! ", minimum_position, end),
            text.rfind(" ", minimum_position, end)
        ]

        best_boundary = max(boundaries)

        if best_boundary >= minimum_position:
            # Include the sentence-ending punctuation,
            # but leave the following whitespace for overlap.
            if text[best_boundary:best_boundary + 1] in ".?!":
                return best_boundary + 1

            return best_boundary

        return end

    def chunk_pages(self, pages: list[dict]) -> list[dict]:

        """
        Convert extracted PDF pages into overlapping chunks.
        Every chunk retains its original PDF page number.
        """

        chunks = []

        for page in pages:

            page_number = page["page_number"]
            text = page["text"].strip()

            if not text:
                continue

            start = 0

            while start < len(text):

                end = min(
                    start + self.chunk_size,
                    len(text)
                )

                # Find a natural boundary when possible.
                if end < len(text):
                    end = self._find_boundary(
                        text, start, end
                    )

                chunk_text = text[start:end].strip()

                if chunk_text:

                    chunks.append({
                        "chunk_id": len(chunks),
                        "page_number": page_number,
                        "text": chunk_text
                    })

                if end >= len(text):
                    break

                # Move forward while retaining overlap.
                next_start = end - self.chunk_overlap

                # Ensure the loop always makes progress.
                start = max(start + 1, next_start)

        return chunks

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    page_number: int = 1,
) -> list[dict]:
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunker.chunk_pages([{"page_number": page_number, "text": text}])