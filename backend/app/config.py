import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set")

if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY is not set")