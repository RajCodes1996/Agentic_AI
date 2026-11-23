
import pytest

from src.pipeline.rag_answer_service import RAGAnswerService

class FakeRetriever:

    def __init__(self, chunks=None):
        self.chunks = chunks or []
        self.last_query = None
        self.last_top_k = None

    def search(self, query, top_k=3):
        self.last_query = query
        self.last_top_k = top_k
        return self.chunks

class FakeLLMProvider:

    def __init__(self, response="Python is a programming language."):
        self.response = response
        self.last_prompt = None
        self.last_system_instruction = None

    def generate(self, prompt, system_instruction=None):
        self.last_prompt = prompt
        self.last_system_instruction = system_instruction
        return self.response

@pytest.fixture
def sample_chunks():
    return [
        {
            "id": "chunk_0",
            "chunk_id": 0,
            "page_number": 1,
            "text": "Python is a high-level programming language.",
            "distance": 0.12
        },
        {
            "id": "chunk_1",
            "chunk_id": 1,
            "page_number": 2,
            "text": "Python supports object-oriented programming.",
            "distance": 0.24
        }
    ]

def test_generate_grounded_answer(sample_chunks):
    retriever = FakeRetriever(sample_chunks)
    provider = FakeLLMProvider()

    service = RAGAnswerService(retriever, provider)

    result = service.answer("What is Python?")

    assert result["answer"] == (
        "Python is a programming language."
    )

    assert result["question"] == "What is Python?"
    assert len(result["sources"]) == 2

def test_page_numbers_are_in_prompt(sample_chunks):
    retriever = FakeRetriever(sample_chunks)
    provider = FakeLLMProvider()

    service = RAGAnswerService(retriever, provider)

    service.answer("What is Python?")

    assert "Page 1" in provider.last_prompt
    assert "Page 2" in provider.last_prompt

def test_system_instruction_is_passed(sample_chunks):
    retriever = FakeRetriever(sample_chunks)
    provider = FakeLLMProvider()

    service = RAGAnswerService(retriever, provider)

    service.answer("What is Python?")

    assert "only the supplied document context" in (
        provider.last_system_instruction
    )

def test_empty_question():
    service = RAGAnswerService(
        FakeRetriever(),
        FakeLLMProvider()
    )

    with pytest.raises(ValueError):
        service.answer("")

def test_invalid_top_k():
    service = RAGAnswerService(
        FakeRetriever(),
        FakeLLMProvider()
    )

    with pytest.raises(ValueError):
        service.answer("What is Python?", top_k=0)

def test_no_retrieved_chunks():
    retriever = FakeRetriever()
    provider = FakeLLMProvider()

    service = RAGAnswerService(retriever, provider)

    result = service.answer("What is Python?")

    assert result["sources"] == []
    assert "No relevant information" in result["answer"]

    # The LLM should not be called without retrieved evidence.
    assert provider.last_prompt is None

def test_top_k_is_forwarded(sample_chunks):
    retriever = FakeRetriever(sample_chunks)
    provider = FakeLLMProvider()

    service = RAGAnswerService(retriever, provider)

    service.answer("What is Python?", top_k=2)

    assert retriever.last_top_k == 2