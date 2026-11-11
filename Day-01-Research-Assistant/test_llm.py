
from llm_client import generate_response


prompt = """
You are an AI research assistant.

Explain Generative AI in 5 simple points.
"""


provider = input(
    "Select provider (ollama/gemini): "
).strip().lower()


try:

    response = generate_response(
        prompt=prompt,
        provider=provider
    )

    print("\nAI RESPONSE:\n")
    print(response)

except Exception as error:

    print("\nERROR:")
    print(error)