from src.retrieval import Retriever, VectorStore

class FakeEmbeddings:
    def embed(self, texts): return [[1.0, 0.0] if "cats" in text else [0.0, 1.0] for text in texts]

def test_retriever_returns_best_match():
    store = VectorStore(); store.add(["cats are mammals", "dogs bark"], [[1, 0], [0, 1]])
    result = Retriever(store, FakeEmbeddings()).retrieve("cats", 1)
    assert result[0]["text"] == "cats are mammals"
