from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY


class TravelDetails(BaseModel):
    origin: str = Field(description="Origin city")
    origin_airport: str = Field(description="3-letter IATA airport code for the origin")
    
    destination: str = Field(description="Destination city")
    destination_airport: str = Field(description="3-letter IATA airport code for the destination")

    days: int = Field(description="Number of travel days")
    travelers: int = Field(description="Number of travelers")
    budget: float = Field(description="Total trip budget")
    preferences: str = Field(description="Travel preferences mentioned by the user")

    departure_date: str = Field(
        description="Trip departure date in YYYY-MM-DD format"
    )

    return_date: str = Field(
        description="Trip return date in YYYY-MM-DD format"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)


structured_llm = llm.with_structured_output(TravelDetails)


def coordinator_agent(user_request: str) -> TravelDetails:

    prompt = f"""
You are the Coordinator Agent for an AI Travel Planner.

Understand the user's travel request and extract all
important travel requirements.

User request:
{user_request}

Extract:

- Origin city
- Origin airport IATA code
- Destination city
- Destination airport IATA code
- Number of days
- Number of travelers
- Total budget
- Travel preferences
- Departure date
- Return date

IMPORTANT:

1. Airport codes must be valid 3-letter IATA codes.

2. Examples:
   Chennai → MAA
   Singapore → SIN
   Bangalore → BLR
   Mumbai → BOM
   Delhi → DEL
   Hyderabad → HYD
   London → LHR
   Paris → CDG

3. Convert dates to YYYY-MM-DD format.

4. If the user provides exact travel dates, extract them.

5. If the user does not provide travel dates, use
   "Not specified" for departure_date and return_date.

6. If a preference is not mentioned, use
   "None specified".

7. Do not invent dates.

User request:
{user_request}
"""

    return structured_llm.invoke(prompt)
