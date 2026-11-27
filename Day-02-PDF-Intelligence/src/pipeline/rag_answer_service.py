import re


class RAGAnswerService:

    SYSTEM_INSTRUCTION = """
You are a strict PDF document question-answering assistant.

Follow these rules without exception:

1. Answer using only the supplied document context.
   Do not use any information outside it.

2. Do not use outside knowledge or assumptions.

3. Do not add explanations, examples, interpretations,
   or ethical conclusions that are not explicitly
   stated in the document.

4. Answer the exact question asked. Do not discuss
   unrelated topics.

5. Keep answers concise: preferably 1-3 sentences.

6. Every factual statement must be supported by
   the supplied document context.

7. Cite the actual page number provided in the
   document context using [Page X].

8. Never invent page numbers.

9. If the document does not contain enough
   information, respond exactly:
   "The uploaded document does not provide enough
   information to answer this."
"""

    OVERVIEW_SYSTEM_INSTRUCTION = """
You are a careful document analyst. Explain documents naturally while staying faithful to their actual contents. Never invent facts or citations.
"""

    MAX_DISTANCE = 0.70

    INSUFFICIENT_INFO = (
        "The uploaded document does not provide enough "
        "information to answer this."
    )

    STOP_WORDS = {
        "the", "a", "an", "is", "are", "was", "were",
        "be", "been", "being", "to", "of", "in", "on",
        "at", "for", "and", "or", "but", "with", "by",
        "from", "as", "it", "this", "that", "these",
        "those", "do", "does", "did", "what", "which",
        "who", "how", "why", "when", "where", "about",
        "their", "they", "them", "we", "you", "your",
        "its", "can", "could", "should", "would"
    }

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

    def _is_answer_supported(
        self,
        answer: str,
        chunks: list[dict]
    ) -> bool:
        """Check whether the answer's content words exist in evidence."""
        answer_words = {
            word.lower()
            for word in re.findall(r"[a-zA-Z0-9]+", answer)
            if len(word) > 2
            and word.lower() not in self.STOP_WORDS
        }
        evidence_text = " ".join(
            chunk["text"] for chunk in chunks
        )
        evidence_words = {
            word.lower()
            for word in re.findall(r"[a-zA-Z0-9]+", evidence_text)
        }
        if not answer_words:
            return False
        return answer_words.issubset(evidence_words)

    def _extractive_fallback(
        self,
        question: str,
        chunks: list[dict]
    ) -> str:
        """Extract relevant original sentences from retrieved chunks."""
        stop_words = self.STOP_WORDS | {
            "mean", "means", "using", "use", "used",
            "explain", "describe", "tell", "define"
        }
        question_words = {
            word.lower()
            for word in re.findall(r"[a-zA-Z0-9]+", question)
            if len(word) > 2 and word.lower() not in stop_words
        }
        if not question_words:
            return self.INSUFFICIENT_INFO

        # Preserve the original chunk order.
        chunks = sorted(
            chunks,
            key=lambda chunk: chunk["chunk_id"]
        )
        candidates = []
        for chunk in chunks:
            # Split on sentence endings, preserving original wording.
            sentences = re.split(
                r"(?<=[.!?])\s+",
                chunk["text"]
            )
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                sentence_words = {
                    word.lower()
                    for word in re.findall(r"[a-zA-Z0-9]+", sentence)
                }
                overlap = len(question_words & sentence_words)
                if overlap > 0:
                    candidates.append((overlap, sentence))

        if not candidates:
            return self.INSUFFICIENT_INFO

        max_overlap = max(overlap for overlap, _ in candidates)
        selected = [
            sentence
            for overlap, sentence in candidates
            if overlap == max_overlap
        ]
        return " ".join(selected[:3])

    def _is_document_overview_question(self, question: str) -> bool:
        """Identify broad questions about the entire uploaded document."""
        normalized = re.sub(r"[^a-z0-9\s]", " ", question.lower())
        normalized = " ".join(normalized.split())
        overview_phrases = (
            "what is in the pdf",
            "what is in this pdf",
            "what is in the document",
            "what does this document contain",
            "what is this document about",
            "summarize this document",
            "summarize the document",
            "summarize this pdf",
            "give me a summary",
            "provide an overview",
            "give me an overview",
            "tell me about this document",
            "explain the document",
            "what are the 4ds",
            "what is the 4ds",
            "explain each of the 4ds",
            "explain the 4ds",
            "describe the 4ds",
            "list the 4ds",
            "tell me about the 4ds"
        )
        return any(
            phrase in normalized
            for phrase in overview_phrases
        )

    def _answer_document_overview(
        self,
        question: str,
        document_pages: list[dict]
    ) -> dict:
        """Generate an overview from the original extracted PDF pages."""
        if not document_pages:
            return {
                "question": question,
                "answer": self.INSUFFICIENT_INFO,
                "sources": []
            }

        # Keep page boundaries so citations remain accurate.
        context_parts = []
        sources = []
        remaining_chars = 12000
        for idx, page in enumerate(document_pages):
            page_text = page.get("text", "").strip()
            if not page_text or remaining_chars <= 0:
                continue
            selected_text = page_text[:remaining_chars]
            page_number = page.get("page_number", idx + 1)
            context_parts.append(
                f"[Page {page_number}]\n{selected_text}"
            )
            sources.append({
                "page_number": page_number,
                "chunk_id": -1,
                "text": selected_text,
                "distance": 0.0
            })
            remaining_chars -= len(selected_text)

        if not context_parts:
            return {
                "question": question,
                "answer": self.INSUFFICIENT_INFO,
                "sources": []
            }

        context = "\n\n".join(context_parts)
        prompt = f"""You are an expert document analysis assistant.
Answer the user's question using ONLY the supplied PDF content.

DOCUMENT CONTENT:
{context}

USER QUESTION:
{question}

IMPORTANT RULES:
1. Describe the actual subject and main ideas of the document.
2. Never invent a document title, author, organization,
   date, statistic, or other detail.
3. Only mention a title if it is explicitly present
   in the supplied document content.
4. Distinguish explicit document facts from interpretations.
5. Do not assume information that is merely suggested.
6. Organize the response into readable paragraphs
   or bullet points.
7. Explain the important concepts in natural,
   conversational language.
8. Every factual statement must be supported
   by the supplied content.
9. Cite the original page numbers using [Page X].
10. If the document does not establish something,
    clearly acknowledge that limitation.

Be helpful, clear and natural, but never sacrifice
accuracy for a more impressive answer."""

        try:
            answer = self.llm_provider.generate(
                prompt=prompt,
                system_instruction=(
                    "You are a careful document analyst. "
                    "Explain documents naturally while staying "
                    "faithful to their actual contents. "
                    "Never invent facts or citations."
                )
            )
        except TypeError as error:
            if "system_instruction" not in str(error):
                raise

            answer = self.llm_provider.generate(prompt)

        answer = str(answer).strip()
        if not answer:
            return {
                "question": question,
                "answer": self.INSUFFICIENT_INFO,
                "sources": []
            }

        # Reject generated overviews containing unsupported terms.
        if not self._is_answer_supported(answer, sources):
            answer = (
                "Here is the information extracted directly "
                "from your document:\n\n"
                + context
            )
        elif not re.search(r"\[Page\s+\d+\]", answer):
            allowed_pages = sorted({source["page_number"] for source in sources})
            citations = " ".join(f"[Page {page}]" for page in allowed_pages)
            answer = f"{answer} {citations}".strip()

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }

    def answer(
        self,
        question: str,
        top_k: int = 3,
        document_pages: list[dict] | None = None
    ) -> dict:
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

        # Handle broad questions using the complete extracted document.
        if (
            document_pages
            and self._is_document_overview_question(question)
        ):
            return self._answer_document_overview(
                question,
                document_pages
            )

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

        # Check whether the best retrieved result is relevant enough.
        best_distance = min(
            chunk["distance"] for chunk in chunks
        )
        if best_distance > self.MAX_DISTANCE:
            return {
                "question": question,
                "answer": (
                    "The uploaded document does not provide enough "
                    "information to answer this."
                ),
                "sources": []
            }

        # Keep only chunks that satisfy the relevance threshold.
        chunks = [
            chunk for chunk in chunks
            if chunk["distance"] <= self.MAX_DISTANCE
        ]

        # Step 3: Build evidence context.
        context = self._build_context(chunks)
        allowed_pages = sorted({chunk["page_number"] for chunk in chunks})
        allowed_pages_text = ", ".join(str(page) for page in allowed_pages)

        # Step 4: Build the LLM prompt.
        prompt = f"""You are an intelligent PDF document assistant.

DOCUMENT CONTEXT:
{context}

AVAILABLE PAGE NUMBERS:
{allowed_pages_text}

USER QUESTION:
{question}

INSTRUCTIONS:

1. Answer the exact question using the document context.
2. Write naturally, clearly and conversationally.
3. If the user asks for a list, identify ALL relevant items.
4. If the user asks about multiple concepts, address EACH concept.
5. Never omit an important item just to keep the answer short.
6. Explain concepts using their definitions in the document.
7. Organize multi-part answers using numbered lists or bullet points.
8. Do not repeat the same concept unnecessarily.
9. Never invent information or use outside knowledge.
10. Cite the actual page numbers using [Page X].
11. Only use page numbers from AVAILABLE PAGE NUMBERS.
12. If the document genuinely lacks the requested information,
    respond exactly:
    "The uploaded document does not provide enough information to answer this."

Produce a complete, useful answer rather than a vague summary.
"""

        # Step 5: Generate the answer.
        try:
            generated_answer = self.llm_provider.generate(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )
        except TypeError as error:
            if "system_instruction" not in str(error):
                raise

            generated_answer = self.llm_provider.generate(prompt)

        # Remove citations before checking factual content.
        generated_answer = re.sub(
            r"\s*\[Page\s+\d+\]",
            "",
            generated_answer
        ).strip()
        # Use extractive fallback when the generated answer has unsupported words.
        if not self._is_answer_supported(generated_answer, chunks):
            generated_answer = self._extractive_fallback(
                question,
                chunks
            )

        if generated_answer == self.INSUFFICIENT_INFO:
            sources = []
            return {
                "question": question,
                "answer": generated_answer,
                "sources": sources
            }

        # Validate citations against retrieved source pages.
        allowed_pages = sorted({
            chunk["page_number"] for chunk in chunks
        })
        # Add citations using actual retrieved page numbers.
        citations = " ".join(
            f"[Page {page}]" for page in allowed_pages
        )
        generated_answer = f"{generated_answer} {citations}"

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