import os
import ollama

from src.llm.base import BaseLLM


class OllamaProvider(BaseLLM):

    def __init__(self, model_name: str | None = None, client=None):
        self.model_name = (
            model_name
            or os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        )

        # Client injection makes testing possible without a live server.
        self.client = client if client is not None else ollama.Client()

    def generate(
        self,
        prompt: str,
        system_instruction: str | None = None
    ) -> str:

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        messages = []

        if system_instruction and system_instruction.strip():
            messages.append({
                "role": "system",
                "content": system_instruction.strip()
            })

        messages.append({
            "role": "user",
            "content": prompt.strip()
        })

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )

            content = response.message.content

        except Exception as exc:
            raise RuntimeError(
                f"Ollama generation failed. Check that Ollama is "
                f"running and model '{self.model_name}' is available."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Ollama returned an empty response.")

        return content.strip()