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
            data.get("error", "SerpApi hotel search failed")
        )

    return data


@tool
def search_hotels(
    destination: str,
    check_in_date: str,
    check_out_date: str,
    travelers: int,
) -> List[Dict]:
    """
    Search real hotels using SerpApi Google Hotels.
    """

    params = {
        "engine": "google_hotels",
        "api_key": SERPAPI_KEY,
        "q": destination,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "adults": travelers,
        "children": 0,
        "currency": "INR",
        "gl": "in",
        "hl": "en",
        "sort_by": 3,
    }

    data = _search_serpapi(params)

    properties = data.get("properties", [])

    results = []

    for hotel in properties:

        rate_per_night = hotel.get("rate_per_night", {})
        total_rate = hotel.get("total_rate", {})

        extracted_nightly = rate_per_night.get(
            "extracted_lowest"
        )

        extracted_total = total_rate.get(
            "extracted_lowest"
        )

        if not extracted_total:
            continue

        results.append({
            "name": hotel.get("name"),
            "location": destination,

            "description": hotel.get("description"),

            "property_token": hotel.get("property_token"),

            "price_per_night": extracted_nightly,
            "total_price": extracted_total,

            "rating": hotel.get("overall_rating"),
            "reviews": hotel.get("reviews"),

            "hotel_class": hotel.get("hotel_class"),

            "check_in_time": hotel.get("check_in_time"),
            "check_out_time": hotel.get("check_out_time"),

            "amenities": hotel.get("amenities", []),

            "gps_coordinates": hotel.get(
                "gps_coordinates"
            ),

            "nearby_places": hotel.get(
                "nearby_places", []
            ),

            "image": (
                hotel.get("images", [{}])[0]
                .get("thumbnail")
                if hotel.get("images")
                else None
            ),

            "link": hotel.get("link"),

            "source": "SerpApi Google Hotels",
            "live_api": True,
        })

    return results[:10]