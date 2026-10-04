from typing import Dict, List, TypedDict


class TravelState(TypedDict):
    user_request: str

    origin: str
    origin_airport: str

    destination: str
    destination_airport: str

    days: int
    travelers: int
    budget: float
    preferences: str

    departure_date: str
    return_date: str

    flight_options: List[Dict]
    hotel_options: List[Dict]
    activity_options: List[Dict]

    budget_analysis: Dict

    itinerary: Dict