import json
import requests

from app.config import SERPAPI_KEY


params = {
    "engine": "google_flights",
    "api_key": SERPAPI_KEY,

    "departure_id": "MAA",
    "arrival_id": "SIN",

    "outbound_date": "2026-10-15",
    "return_date": "2026-10-19",

    "type": "1",
    "travel_class": "1",
    "adults": 2,

    "currency": "INR",
    "gl": "in",
    "hl": "en",
}


response = requests.get(
    "https://serpapi.com/search",
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()

print(json.dumps(data, indent=2))