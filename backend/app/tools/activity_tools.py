from typing import List, Dict
import requests

from langchain_core.tools import tool

from app.config import SERPAPI_KEY


SERPAPI_URL = "https://serpapi.com/search"


def _search_serpapi(params: Dict) -> Dict:
    response = requests.get(
        SERPAPI_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("search_metadata", {}).get("status") != "Success":
        raise RuntimeError(
            data.get("error", "SerpApi activity search failed")
        )

    return data


@tool
def search_activities(
    destination: str,
    preferences: str,
    days: int,
    travelers: int,
) -> List[Dict]:
    """
    Search real attractions and activities using Google Maps.
    """

    query = (
        f"tourist attractions activities {destination} "
        f"{preferences}"
    )

    params = {
        "engine": "google_maps",
        "type": "search",
        "api_key": SERPAPI_KEY,
        "q": query,
        "hl": "en",
        "gl": "in",
        "start": 0,
    }

    data = _search_serpapi(params)

    local_results = data.get("local_results", [])

    print("\n========== RAW ACTIVITY RESULTS ==========\n")

    for place in local_results[:3]:
        print(place)

    activities = []

    for place in local_results:

        name = place.get("title")

        if not name:
            continue

        activities.append({
            "name": name,

            "description": place.get("description"),

            "location": place.get("address"),

            "type": place.get("type"),

            "rating": place.get("rating"),

            "reviews": place.get("reviews"),

            "gps_coordinates": place.get(
                "gps_coordinates"
            ),

            "image": place.get("thumbnail"),

            "link": place.get("website"),

            # Google Maps search does not give us
            # reliable standardized ticket prices.
            "price_per_person": None,
            "price_available": False,

            "source": "SerpApi Google Maps",

            "live_api": True,
        })

        if len(activities) >= 10:
            break

    return activities