import os

from google import genai
from google.genai import types

from src.llm.base import BaseLLM


class GeminiProvider(BaseLLM):

    def __init__(
        self,
        model_name: str | None = None,
        api_key: str | None = None,
        client=None
    ):

        self.model_name = (
            model_name
            or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        )

        if client is not None:
            self.client = client
        else:
            resolved_api_key = api_key or os.getenv("GEMINI_API_KEY")

            if not resolved_api_key:
                raise ValueError(
                    "GEMINI_API_KEY is missing. Add it to your .env file."
                )

            self.client = genai.Client(api_key=resolved_api_key)

    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None
    ) -> str:

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            config = None

            if system_instruction and system_instruction.strip():
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction.strip()
                )

            if config is None:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt.strip()
                )
            else:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt.strip(),
                    config=config
                )

            content = response.text

        except Exception as exc:
            raise RuntimeError(
                "Gemini generation failed. Check your API key, "
                "model availability, and network connection."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return content.strip()