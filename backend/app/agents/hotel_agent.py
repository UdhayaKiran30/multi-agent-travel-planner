from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY
from app.graph.state import TravelState
from app.tools.hotel_tools import search_hotels


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

llm_with_tools = llm.bind_tools([search_hotels])


def hotel_agent(state: TravelState):

    prompt = f"""
You are the Hotel Agent in a multi-agent AI Travel Planner.

The user wants to travel to:

Destination: {state["destination"]}

Number of travelers: {state["travelers"]}

Check-in date: {state["departure_date"]}

Check-out date: {state["return_date"]}

Your task is to retrieve real hotel options.

Use the search_hotels tool.

IMPORTANT RULES:
1. Use the exact destination provided by the user.
2. Use the exact number of travelers.
3. Use the exact check-in date.
4. Use the exact check-out date.
5. Do NOT invent hotel information.
6. Do NOT create hotel options yourself.
7. Return only data obtained from the hotel search tool.
"""

    response = llm_with_tools.invoke(prompt)

    if response.tool_calls:

        tool_call = response.tool_calls[0]

        tool_args = tool_call["args"]

        # Ensure the tool receives the exact values
        # extracted by the Coordinator Agent.
        tool_args["destination"] = state["destination"]
        tool_args["check_in_date"] = state["departure_date"]
        tool_args["check_out_date"] = state["return_date"]
        tool_args["travelers"] = state["travelers"]

        tool_result = search_hotels.invoke(tool_args)

        return {
            "hotel_options": tool_result
        }

    return {
        "hotel_options": []
    }
