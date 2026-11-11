
from tools import search_web


query = "Latest developments in Generative AI 2026"

try:

    results = search_web(
        query=query,
        max_results=5
    )

    print("\nSEARCH RESULTS\n")

    for number, result in enumerate(results, start=1):

        print(f"\nSOURCE {number}")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Score:", result["score"])
        print("Content:", result["content"][:500])
        print("-" * 60)

except Exception as error:

    print("ERROR:", error)
