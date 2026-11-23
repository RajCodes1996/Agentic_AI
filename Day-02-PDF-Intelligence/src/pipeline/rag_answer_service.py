
class RAGAnswerService:

    SYSTEM_INSTRUCTION = """
You are a PDF document question-answering assistant.

Follow these rules strictly:

1. Answer using only the supplied document context.
2. Do not invent facts or use outside knowledge.
3. If the context does not contain the answer, clearly say:
   "The uploaded document does not provide enough information to answer this."
4. Cite the page number whenever you use information from a passage.
5. Use citations in this format: [Page 3].
6. If multiple pages support the answer, cite all relevant pages.
7. Explain the answer clearly and directly.
"""

    def __init__(self, retriever, llm_provider):
        self.retriever = retriever
        self.llm_provider = llm_provider

    def _build_context(self, chunks: list[dict]) -> str:
        """Format retrieved passages with their original page numbers."""

        context_parts = []

        for index, chunk in enumerate(chunks, start=1):
            context_parts.append(
                f"[Passage {index} | Page {chunk['page_number']}]\n"
                f"{chunk['text']}"
            )

        return "\n\n".join(context_parts)

    def answer(self, question: str, top_k: int = 3) -> dict:
        """Retrieve relevant passages and generate a grounded answer."""

        if not isinstance(question, str) or not question.strip():
            raise ValueError("Question cannot be empty.")

        if (
            not isinstance(top_k, int)
            or isinstance(top_k, bool)
            or top_k <= 0
        ):
            raise ValueError("top_k must be a positive integer.")

        question = question.strip()

        # Step 1: Retrieve relevant PDF passages.
        chunks = self.retriever.search(
            query=question,
            top_k=top_k
        )

        # Step 2: Handle an empty retrieval result.
        if not chunks:
            return {
                "question": question,
                "answer": (
                    "No relevant information was found in the "
                    "uploaded document."
                ),
                "sources": []
            }

        # Step 3: Build evidence context.
        context = self._build_context(chunks)

        # Step 4: Build the LLM prompt.
        prompt = f"""
DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

INSTRUCTIONS:

Answer the question using only the document context.
Include page citations in the format [Page X].
If the answer is not available in the context, say so clearly.
"""

        # Step 5: Generate the answer.
        generated_answer = self.llm_provider.generate(
            prompt=prompt,
            system_instruction=self.SYSTEM_INSTRUCTION
        )

        # Step 6: Return answer and source information.
        sources = [
            {
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "distance": chunk["distance"]
            }
            for chunk in chunks
        ]

        return {
            "question": question,
            "answer": generated_answer,
            "sources": sources
        }