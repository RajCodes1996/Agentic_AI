
from types import SimpleNamespace

import pytest

from src.llm.ollama_provider import OllamaProvider
from src.llm.gemini_provider import GeminiProvider
from src.llm.provider_factory import create_llm_provider

class FakeOllamaClient:

    def __init__(self, content="Ollama test response"):
        self.content = content
        self.last_call = None

    def chat(self, **kwargs):
        self.last_call = kwargs

        return SimpleNamespace(
            message=SimpleNamespace(content=self.content)
        )

class FakeGeminiModels:

    def __init__(self, content="Gemini test response"):
        self.content = content
        self.last_call = None

    def generate_content(self, **kwargs):
        self.last_call = kwargs
        return SimpleNamespace(text=self.content)

class FakeGeminiClient:

    def __init__(self, content="Gemini test response"):
        self.models = FakeGeminiModels(content)

def test_ollama_generation():
    client = FakeOllamaClient()
    provider = OllamaProvider(client=client)

    result = provider.generate("Explain Python.")

    assert result == "Ollama test response"
    assert client.last_call["messages"][-1]["content"] == "Explain Python."

def test_ollama_system_instruction():
    client = FakeOllamaClient()
    provider = OllamaProvider(client=client)

    provider.generate(
        "Explain Python.",
        system_instruction="You are a helpful tutor."
    )

    messages = client.last_call["messages"]

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a helpful tutor."

def test_ollama_empty_prompt():
    provider = OllamaProvider(client=FakeOllamaClient())

    with pytest.raises(ValueError):
        provider.generate("")

def test_ollama_empty_response():
    provider = OllamaProvider(
        client=FakeOllamaClient(content="")
    )

    with pytest.raises(RuntimeError):
        provider.generate("Hello")

def test_gemini_generation():
    client = FakeGeminiClient()
    provider = GeminiProvider(client=client)

    result = provider.generate("Explain Python.")

    assert result == "Gemini test response"
    assert client.models.last_call["contents"] == "Explain Python."

def test_gemini_system_instruction():
    client = FakeGeminiClient()
    provider = GeminiProvider(client=client)

    provider.generate(
        "Explain Python.",
        system_instruction="You are a helpful tutor."
    )

    config = client.models.last_call["config"]

    assert config.system_instruction == "You are a helpful tutor."

def test_gemini_empty_prompt():
    provider = GeminiProvider(client=FakeGeminiClient())

    with pytest.raises(ValueError):
        provider.generate("")

def test_gemini_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError):
        GeminiProvider()

def test_factory_ollama():
    provider = create_llm_provider(
        "ollama",
        client=FakeOllamaClient()
    )

    assert isinstance(provider, OllamaProvider)

def test_factory_gemini():
    provider = create_llm_provider(
        "gemini",
        client=FakeGeminiClient()
    )

    assert isinstance(provider, GeminiProvider)

def test_factory_invalid_provider():
    with pytest.raises(ValueError):
        create_llm_provider("unknown")