import json
import requests

from app.config import SERPAPI_KEY


DEPARTURE_TOKEN = "WyJDalJJTnpCVFRWWmZiV2xKWVVWQlMybzNibWRDUnkwdExTMHRMVzlyZEhBeU15MXVNa0ZCUVVGQlIzSkJibFZGVGxoaFZtOUJFZzAyUlRjeE9UbDhOa1V4TURBM0dnc0kvT29FRUFBYUEwbE9VamdjY09tREJRPT0iLFtbIk1BQSIsIjIwMjYtMTAtMTUiLCJUUloiLG51bGwsIjZFIiwiNzE5OSJdLFsiVFJaIiwiMjAyNi0xMC0xNSIsIlNJTiIsbnVsbCwiNkUiLCIxMDA3Il1dXQ=="


params = {
    "engine": "google_flights",
    "api_key": SERPAPI_KEY,

    # Original search information
    "departure_id": "MAA",
    "arrival_id": "SIN",
    "outbound_date": "2026-10-15",
    "return_date": "2026-10-19",

    "type": "1",
    "travel_class": "1",
    "adults": 2,

    # Token selects the specific outbound flight
    "departure_token": DEPARTURE_TOKEN,

    "currency": "INR",
    "gl": "in",
    "hl": "en",
}


response = requests.get(
    "https://serpapi.com/search",
    params=params,
    timeout=30,
)

print("Status code:", response.status_code)

if not response.ok:
    print(response.text)

response.raise_for_status()

data = response.json()

print(json.dumps(data, indent=2))