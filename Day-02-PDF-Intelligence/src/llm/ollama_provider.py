from .base import BaseLLM

class OllamaProvider(BaseLLM):
    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            import ollama
            return ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])["message"]["content"]
        except Exception as exc:
            raise RuntimeError(f"Ollama generation failed: {exc}") from exc
