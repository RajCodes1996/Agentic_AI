from src.pipeline import RAGPipeline

class FakeEmbeddings:
    def embed(self, texts): return [[float(len(text)), 1.0] for text in texts]
class FakeLLM:
    def generate(self, prompt): return "grounded answer"

def test_pipeline_indexes_and_answers():
    pipeline = RAGPipeline(FakeLLM(), FakeEmbeddings(), chunk_size=30, chunk_overlap=5)
    assert pipeline.index("A short document about RAG systems.") >= 1
    answer, sources = pipeline.answer("What is it?")
    assert answer == "grounded answer" and sources
