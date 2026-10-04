from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY
from app.graph.state import TravelState
from app.tools.currency_tools import convert_currency


class BudgetDecision(BaseModel):
    selected_flight_index: int = Field(
        description="Index of the selected flight option"
    )

    selected_hotel_index: int = Field(
        description="Index of the selected hotel option"
    )

    selected_activity_indices: List[int] = Field(
        description="Indices of selected activity options"
    )

    reasoning: str = Field(
        description="Short explanation for the selection"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

structured_llm = llm.with_structured_output(BudgetDecision)


def budget_agent(state: TravelState):

    flights = state["flight_options"]
    hotels = state["hotel_options"]
    activities = state["activity_options"]

    budget = state["budget"]
    travelers = state["travelers"]

    # -----------------------------
    # Add indexes for LLM selection
    # -----------------------------

    indexed_flights = [
        {
            "index": i,
            **flight
        }
        for i, flight in enumerate(flights)
    ]

    indexed_hotels = [
        {
            "index": i,
            **hotel
        }
        for i, hotel in enumerate(hotels)
    ]

    indexed_activities = [
        {
            "index": i,
            **activity
        }
        for i, activity in enumerate(activities)
    ]

    prompt = f"""
You are the Budget Agent in a multi-agent AI Travel Planner.

Your job is to select travel options based on:
- User budget
- Number of travelers
- Travel preferences

TRIP DETAILS
------------
Budget: ₹{budget}
Travelers: {travelers}
Days: {state["days"]}
Preferences: {state["preferences"]}

FLIGHT OPTIONS
--------------
{indexed_flights}

HOTEL OPTIONS
-------------
{indexed_hotels}

ACTIVITY OPTIONS
----------------
{indexed_activities}

RULES
-----
1. Select exactly ONE flight using its index.
2. Select exactly ONE hotel using its index.
3. Select up to THREE activities using their indices.
4. Prefer options that match the user's preferences.
5. Prefer affordable options.
6. ONLY select options from the provided lists.
7. NEVER invent an option.
8. The flight total_price already includes all travelers.
9. The hotel total_price is the complete hotel cost.
10. Activity price_per_person is for ONE traveler.
11. Activity prices may be in currencies such as SGD.
12. Python will convert activity prices to INR.
13. Python will calculate the final cost.
14. Do NOT perform final arithmetic yourself.
15. If some activity prices are unavailable, Python will
    mark the final trip cost as unavailable.

Return only the structured recommendation.
"""

    decision = structured_llm.invoke(prompt)

    # -----------------------------
    # Validate selected indexes
    # -----------------------------

    flight_index = decision.selected_flight_index
    hotel_index = decision.selected_hotel_index

    if not 0 <= flight_index < len(flights):
        flight_index = 0

    if not 0 <= hotel_index < len(hotels):
        hotel_index = 0

    selected_flight = flights[flight_index]
    selected_hotel = hotels[hotel_index]

    selected_activities = []

    for index in decision.selected_activity_indices[:3]:
        if 0 <= index < len(activities):
            selected_activities.append(activities[index])

    # -----------------------------
    # Flight cost
    # -----------------------------

    flight_cost = selected_flight["total_price"]

    # -----------------------------
    # Hotel cost
    # -----------------------------

    hotel_cost = selected_hotel["total_price"]

    # -----------------------------
    # Activity cost
    # -----------------------------

    activity_cost = 0.0
    activity_pricing_available = True

    activity_breakdown = []

    for activity in selected_activities:

        price = activity.get("price_per_person")
        currency = activity.get("currency")

        # No price available
        if price is None:
            activity_pricing_available = False
            break

        # Convert non-INR currencies
        if currency and currency.upper() != "INR":

            converted_price = convert_currency.invoke({
                "amount": price,
                "from_currency": currency.upper(),
                "to_currency": "INR",
            })

            if converted_price is None:
                activity_pricing_available = False
                break

            price_inr = converted_price

        else:
            price_inr = price

        total_activity_price = price_inr * travelers

        activity_cost += total_activity_price

        activity_breakdown.append({
            "name": activity["name"],
            "price_per_person": price,
            "currency": currency,
            "price_inr": round(price_inr, 2),
            "travelers": travelers,
            "total_cost": round(total_activity_price, 2),
        })

    # -----------------------------
    # Final budget calculation
    # -----------------------------

    known_cost = flight_cost + hotel_cost

    if activity_pricing_available:

        total_cost = known_cost + activity_cost

        remaining_budget = budget - total_cost

        within_budget = total_cost <= budget

        activity_pricing_status = "Available"

    else:

        activity_cost = None
        total_cost = None
        remaining_budget = None
        within_budget = None

        activity_pricing_status = "Partially unavailable"

    # -----------------------------
    # Reasoning
    # -----------------------------

    reasoning = (
        f"Selected {selected_flight['airline']} flight at "
        f"₹{flight_cost}, {selected_hotel['name']} at "
        f"₹{hotel_cost}, and {len(selected_activities)} activities "
        f"based on the user's budget and preferences."
    )

    if total_cost is not None:
        reasoning += (
            f" The calculated total is ₹{round(total_cost, 2)} "
            f"against a budget of ₹{budget}."
        )
    else:
        reasoning += (
            " The complete trip cost could not be calculated "
            "because one or more selected activities do not have "
            "reliable pricing."
        )

    if within_budget is True:

        budget_status = (
            "The selected combination is within the user's budget."
        )

    elif within_budget is False:

        budget_status = (
            "The selected combination exceeds the user's budget "
            "based on the available pricing."
        )

    else:

        budget_status = (
            "The complete budget status cannot be determined "
            "because activity pricing is unavailable."
        )

    # -----------------------------
    # Return state
    # -----------------------------

    return {
        "budget_analysis": {

            "flight_cost": flight_cost,

            "hotel_cost": hotel_cost,

            "activity_cost": (
                round(activity_cost, 2)
                if activity_cost is not None
                else None
            ),

            "activity_pricing_status": activity_pricing_status,

            "activity_breakdown": activity_breakdown,

            "known_cost": round(known_cost, 2),

            "total_cost": (
                round(total_cost, 2)
                if total_cost is not None
                else None
            ),

            "budget": budget,

            "remaining_budget": (
                round(remaining_budget, 2)
                if remaining_budget is not None
                else None
            ),

            "within_budget": within_budget,

            "selected_flight": selected_flight,

            "selected_hotel": selected_hotel,

            "selected_activities": selected_activities,

            "reasoning": reasoning,

            "budget_status": budget_status,
        }
    }
