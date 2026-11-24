
from dotenv import load_dotenv

from src.llm.ollama_provider import OllamaProvider

load_dotenv()

print("Initializing Ollama provider...")

provider = OllamaProvider()

print(f"Selected model: {provider.model_name}")
print("Sending test prompt...\n")

try:
    response = provider.generate(
        prompt="Explain what Retrieval Augmented Generation (RAG) is in simple terms.",
        system_instruction=(
            "You are a helpful AI assistant. "
            "Answer in simple English."
        )
    )

    print("OLLAMA RESPONSE:")
    print("-" * 50)
    print(response)
    print("-" * 50)

    print("\nLive Ollama integration successful!")

except Exception as error:
    print("\nOllama integration failed.")
    print(f"Error: {error}")
