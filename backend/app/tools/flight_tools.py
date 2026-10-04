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
            data.get("error", "SerpApi search failed")
        )

    return data


def _parse_leg(flights: List[Dict]) -> Dict:
    """
    Convert SerpApi flight segments into our application format.
    """

    if not flights:
        return {}

    first_segment = flights[0]
    last_segment = flights[-1]

    departure = first_segment.get(
        "departure_airport",
        {}
    )

    arrival = last_segment.get(
        "arrival_airport",
        {}
    )

    return {
        "route": (
            f'{departure.get("id", "")} '
            f'→ {arrival.get("id", "")}'
        ),

        "departure_airport": departure.get("name"),

        "departure_airport_code": departure.get("id"),

        "departure_time": departure.get("time"),

        "arrival_airport": arrival.get("name"),

        "arrival_airport_code": arrival.get("id"),

        "arrival_time": arrival.get("time"),

        "duration_minutes": sum(
            segment.get("duration", 0)
            for segment in flights
        ),

        "stops": max(len(flights) - 1, 0),

        "segments": [
            {
                "airline": segment.get("airline"),

                "flight_number": segment.get(
                    "flight_number"
                ),

                "airplane": segment.get(
                    "airplane"
                ),

                "departure": segment.get(
                    "departure_airport"
                ),

                "arrival": segment.get(
                    "arrival_airport"
                ),

                "duration_minutes": segment.get(
                    "duration"
                ),
            }

            for segment in flights
        ],
    }


def _get_return_flights(
    departure_token: str,
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str,
    travelers: int,
) -> Dict:

    params = {
        "engine": "google_flights",
        "api_key": SERPAPI_KEY,

        "departure_id": origin,
        "arrival_id": destination,

        "outbound_date": departure_date,
        "return_date": return_date,

        "type": "1",

        "travel_class": "1",

        "adults": travelers,

        "departure_token": departure_token,

        "currency": "INR",
        "gl": "in",
        "hl": "en",
    }

    return _search_serpapi(params)


@tool
def search_flights(
    origin: str,
    destination: str,
    travelers: int,
    departure_date: str,
    return_date: str,
) -> List[Dict]:
    """
    Search real round-trip flights using SerpApi Google Flights.
    """

    # ------------------------------------------------
    # STEP 1: Search outbound flights
    # ------------------------------------------------

    params = {
        "engine": "google_flights",
        "api_key": SERPAPI_KEY,

        "departure_id": origin,
        "arrival_id": destination,

        "outbound_date": departure_date,
        "return_date": return_date,

        "type": "1",

        "travel_class": "1",

        "adults": travelers,

        "currency": "INR",
        "gl": "in",
        "hl": "en",
    }

    data = _search_serpapi(params)

    raw_flights = (
        data.get("best_flights", [])
        + data.get("other_flights", [])
    )

    results = []

    # ------------------------------------------------
    # STEP 2: Process outbound flights
    # ------------------------------------------------

    for flight_option in raw_flights:

        outbound_segments = flight_option.get(
            "flights",
            []
        )

        if not outbound_segments:
            continue

        total_price = flight_option.get(
            "price"
        )

        if not total_price or total_price <= 0:
            continue

        departure_token = flight_option.get(
            "departure_token"
        )

        if not departure_token:
            continue

        # Parse outbound
        outbound = _parse_leg(
            outbound_segments
        )

        # ------------------------------------------------
        # STEP 3: Get return flights
        # ------------------------------------------------

        return_data = _get_return_flights(
            departure_token=departure_token,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            travelers=travelers,
        )

        return_options = (
            return_data.get("best_flights", [])
            + return_data.get("other_flights", [])
        )

        if not return_options:
            continue

        # ------------------------------------------------
        # STEP 4: Select first valid return option
        # ------------------------------------------------

        selected_return = None

        for return_option in return_options:

            return_segments = return_option.get(
                "flights",
                []
            )

            if return_segments:
                selected_return = return_option
                break

        if not selected_return:
            continue

        return_segments = selected_return.get(
            "flights",
            []
        )

        return_leg = _parse_leg(
            return_segments
        )

        # ------------------------------------------------
        # STEP 5: Create complete round-trip object
        # ------------------------------------------------

        airline = outbound_segments[0].get(
            "airline",
            "Unknown"
        )

        results.append({

            "airline": airline,

            "airline_logo": flight_option.get(
                "airline_logo"
            ),

            "total_price": total_price,

            "price_per_person": round(
                total_price / travelers
            ),

            "departure_date": departure_date,

            "return_date": return_date,

            "outbound": outbound,

            "return": return_leg,

            "type": "Round trip",

            "source": "SerpApi Google Flights",

            "live_api": True,

        })

    return results[:10]