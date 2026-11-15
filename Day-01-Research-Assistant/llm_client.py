
import os

import ollama
from google import genai
from dotenv import load_dotenv


load_dotenv()


def generate_response(prompt: str, provider: str) -> str:
    """
    Generate a response using either a local
    Ollama model or the Gemini cloud API.
    """

    if provider == "ollama":

        model = os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5:0.5b"
        )

        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        options={
             "num_thread": 1,   # Reserves 1 core so Windows never freezes
             "num_ctx": 1536    # Keeps RAM usage minimal
         }
        )

        return response.message.content

    elif provider == "gemini":

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from .env"
            )

        model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        client = genai.Client(api_key=api_key)

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if not response.text:
                raise RuntimeError(
                    "The cloud model returned an empty response."
                )

            return response.text

        finally:
            client.close()

    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )