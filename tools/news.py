import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)


def search_news(query: str):
    """
    Search the web for current news.
    """

    response = tavily_client.search(
        query=query,
        topic="news",
        search_depth="advanced",
        max_results=5,
        include_answer=True
    )

    results = []

    for result in response.get("results", []):
        results.append({
            "title": result.get("title"),
            "content": result.get("content"),
            "url": result.get("url")
        })

    return {
        "query": query,
        "answer": response.get("answer"),
        "results": results
    }