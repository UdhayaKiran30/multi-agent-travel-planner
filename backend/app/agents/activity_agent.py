from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY
from app.graph.state import TravelState
from app.tools.activity_tools import search_activities
from app.agents.activity_price_agent import get_activity_price


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

llm_with_tools = llm.bind_tools([search_activities])


def activity_agent(state: TravelState):

    prompt = f"""
You are the Activity Agent in a multi-agent AI Travel Planner.

The user wants to travel to:
{state["destination"]}

Number of travel days:
{state["days"]}

Number of travelers:
{state["travelers"]}

User preferences:
{state["preferences"]}

Use the activity search tool to retrieve real attractions
and activities.

Do not invent activity data.
"""

    response = llm_with_tools.invoke(prompt)

    if not response.tool_calls:
        return {
            "activity_options": []
        }

    tool_call = response.tool_calls[0]

    activities = search_activities.invoke(
        tool_call["args"]
    )

    enriched_activities = []

    for activity in activities:

        price = get_activity_price(
            activity_name=activity["name"],
            destination=state["destination"],
        )

        activity["price_per_person"] = price.price_per_person
        activity["currency"] = price.currency
        activity["price_source"] = price.source_text
        activity["price_available"] = (
            price.price_per_person is not None
        )

        enriched_activities.append(activity)

    return {
        "activity_options": enriched_activities
    }
