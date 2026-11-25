from src.pipeline import RAGPipeline


class FakeEmbeddings:
    def embed(self, texts):
        return [[float(len(text)), 1.0] for text in texts]


class FakeLLM:
    def generate(self, prompt):
        return "grounded answer"


def test_pipeline_indexes_and_answers():
    pipeline = RAGPipeline(
        FakeLLM(),
        FakeEmbeddings(),
        chunk_size=30,
        chunk_overlap=5
    )
    indexed_chunks = pipeline.index(
        "A short document about RAG systems."
    )
    assert indexed_chunks >= 1

    answer, sources = pipeline.answer("What is it?")
    assert answer == (
        "The uploaded document does not provide enough "
        "information to answer this."
    )
    assert sources == []