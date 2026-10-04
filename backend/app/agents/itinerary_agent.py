from typing import List

from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY
from app.graph.state import TravelState


class DayPlan(BaseModel):
    day: int
    morning: str
    afternoon: str
    evening: str


class Itinerary(BaseModel):
    recommended_flight: str
    recommended_hotel: str
    selected_activities: List[str]
    days: List[DayPlan]
    estimated_cost: float | None
    remaining_budget: float | None


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

structured_llm = llm.with_structured_output(Itinerary)


def itinerary_agent(state: TravelState):

    budget_analysis = state["budget_analysis"]

    selected_flight = budget_analysis["selected_flight"]
    selected_hotel = budget_analysis["selected_hotel"]
    selected_activities = budget_analysis["selected_activities"]

    estimated_cost = budget_analysis["total_cost"]
    remaining_budget = budget_analysis["remaining_budget"]

    prompt = f"""
You are the Itinerary Agent in a multi-agent AI Travel Planner.

Create a practical day-by-day travel itinerary.

TRIP DETAILS
------------
Origin: {state["origin"]}
Destination: {state["destination"]}
Departure date: {state["departure_date"]}
Return date: {state["return_date"]}
Days: {state["days"]}
Travelers: {state["travelers"]}
Preferences: {state["preferences"]}

SELECTED FLIGHT
---------------
{selected_flight}

SELECTED HOTEL
--------------
{selected_hotel}

SELECTED ACTIVITIES
-------------------
{selected_activities}

BUDGET INFORMATION
------------------
Estimated total cost: {estimated_cost}
Remaining budget: {remaining_budget}

IMPORTANT RULES
---------------
1. Use ONLY the selected flight, hotel, and activities.
2. Do NOT invent additional attractions.
3. Do NOT invent prices.
4. Do NOT perform budget calculations.
5. Do NOT modify the estimated cost.
6. Do NOT modify the remaining budget.
7. If estimated total cost is unavailable, keep it unavailable.
8. If remaining budget is unavailable, keep it unavailable.
9. Use the actual flight information provided above.
10. Consider the departure and return dates.
11. Consider flight timings when creating the itinerary.
12. Keep the itinerary realistic and concise.

Return the complete structured itinerary.
"""

    result = structured_llm.invoke(prompt)

    return {
        "itinerary": {
            "recommended_flight": result.recommended_flight,
            "recommended_hotel": result.recommended_hotel,
            "selected_activities": result.selected_activities,
            "days": [
                day.model_dump()
                for day in result.days
            ],
            "estimated_cost": estimated_cost,
            "remaining_budget": remaining_budget,
        }
    }
