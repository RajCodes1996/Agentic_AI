
import os
import requests

from dotenv import load_dotenv


load_dotenv()

TAVILY_URL = "https://api.tavily.com/search"


def search_web(
    query: str,
    max_results: int = 3,
    search_depth: str = "basic"
) -> list:

    """
    Search the web using Tavily.

    Returns structured search results.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is missing from .env"
        )

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= max_results <= 20:
        raise ValueError("max_results must be between 1 and 20.")

    if search_depth not in ["basic", "advanced", "fast", "ultra-fast"]:
        raise ValueError("Invalid search depth.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": False,
        "include_raw_content": False
    }

    try:

        response = requests.post(
            TAVILY_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):

            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score", 0.0),
                "published_date": item.get(
                    "published_date"
                )
            })

        return results

    except requests.RequestException as error:

        raise RuntimeError(
            f"Web search failed: {error}"
        ) from error

    except ValueError as error:

        raise RuntimeError(
            f"Invalid search response: {error}"
        ) from error
        
        
def collect_research_evidence(
    research_questions: list,
    results_per_question: int = 3
) -> list:

    """
    Search every research question and
    combine the collected evidence.
    """

    all_evidence = []
    seen_urls = set()

    for question in research_questions:

        search_results = search_web(
            query=question,
            max_results=results_per_question
        )

        for result in search_results:

            url = result["url"]

            if url and url not in seen_urls:

                seen_urls.add(url)

                result["research_question"] = question

                all_evidence.append(result)

    return all_evidence
