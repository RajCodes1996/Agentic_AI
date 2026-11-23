
from src.llm.ollama_provider import OllamaProvider
from src.llm.gemini_provider import GeminiProvider

def create_llm_provider(provider_name: str, **kwargs):

    if not isinstance(provider_name, str):
        raise ValueError("Provider name must be a string.")

    provider_name = provider_name.strip().lower()

    if provider_name == "ollama":
        return OllamaProvider(**kwargs)

    if provider_name == "gemini":
        return GeminiProvider(**kwargs)

    raise ValueError(
        f"Unsupported LLM provider: {provider_name}. "
        "Choose 'ollama' or 'gemini'."
    ) 