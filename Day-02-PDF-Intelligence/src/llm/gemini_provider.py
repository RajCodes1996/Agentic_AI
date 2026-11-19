from .base import BaseLLM

class GeminiProvider(BaseLLM):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini.")
        self.api_key, self.model = api_key, model

    def generate(self, prompt: str) -> str:
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            return client.models.generate_content(model=self.model, contents=prompt).text
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc
