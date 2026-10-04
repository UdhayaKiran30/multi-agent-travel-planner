from typing import Optional
import requests

from langchain_core.tools import tool

from app.config import SERPAPI_KEY

SERPAPI_URL = "https://serpapi.com/search"


@tool
def search_activity_price(
    activity_name: str,
    destination: str,
) -> Optional[str]:
    """
    Search Google for the current ticket/admission price
    of a specific travel activity.
    """

    query = (
        f'"{activity_name}" {destination} '
        f'official ticket price admission fee'
    )

    params = {
        "engine": "google",
        "api_key": SERPAPI_KEY,
        "q": query,
        "location": destination,
        "num": 5,
        "hl": "en",
        "gl": "sg",
    }

    try:
        response = requests.get(
            SERPAPI_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("search_metadata", {}).get("status") != "Success":
            return None

        results = data.get("organic_results", [])

        if not results:
            return None

        snippets = []

        for result in results[:5]:
            title = result.get("title", "")
            snippet = result.get("snippet", "")

            if title or snippet:
                snippets.append(
                    f"Title: {title}\nSnippet: {snippet}"
                )

        return "\n\n".join(snippets)

    except requests.exceptions.Timeout:
        print(
            f"[WARNING] Price search timed out for: "
            f"{activity_name}"
        )
        return None

    except requests.exceptions.RequestException as e:
        print(
            f"[WARNING] Price search failed for "
            f"{activity_name}: {e}"
        )
        return None

    except Exception as e:
        print(
            f"[WARNING] Unexpected price search error for "
            f"{activity_name}: {e}"
        )
        return None