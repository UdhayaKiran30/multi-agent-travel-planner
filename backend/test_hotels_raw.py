import json
import requests

from app.config import SERPAPI_KEY


params = {
    "engine": "google_hotels",
    "api_key": SERPAPI_KEY,

    "q": "Singapore",

    "check_in_date": "2026-10-15",
    "check_out_date": "2026-10-19",

    "adults": 2,
    "currency": "INR",
    "gl": "in",
    "hl": "en",

    "sort_by": 3,
}


response = requests.get(
    "https://serpapi.com/search",
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()

print(json.dumps(data, indent=2))