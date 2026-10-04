from langgraph.graph import StateGraph, START, END

from app.graph.state import TravelState
from app.agents.coordinator import coordinator_agent
from app.agents.flight_agent import flight_agent
from app.agents.hotel_agent import hotel_agent
from app.agents.activity_agent import activity_agent
from app.agents.budget_agent import budget_agent
from app.agents.itinerary_agent import itinerary_agent


def coordinator_node(state: TravelState):

    travel_details = coordinator_agent(
        state["user_request"]
    )

    return {
        "origin": travel_details.origin,
        "origin_airport": travel_details.origin_airport,

        "destination": travel_details.destination,
        "destination_airport": travel_details.destination_airport,

        "days": travel_details.days,
        "travelers": travel_details.travelers,
        "budget": travel_details.budget,
        "preferences": travel_details.preferences,

        "departure_date": travel_details.departure_date,
        "return_date": travel_details.return_date,
    }

def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node("coordinator", coordinator_node)
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("activity_agent", activity_agent)
    graph.add_node("budget_agent", budget_agent)
    graph.add_node("itinerary_agent", itinerary_agent)

    graph.add_edge(START, "coordinator")

    # Parallel agents
    graph.add_edge("coordinator", "flight_agent")
    graph.add_edge("coordinator", "hotel_agent")
    graph.add_edge("coordinator", "activity_agent")

    # All three converge into Budget Agent
    graph.add_edge("flight_agent", "budget_agent")
    graph.add_edge("hotel_agent", "budget_agent")
    graph.add_edge("activity_agent", "budget_agent")

    # Final planning
    graph.add_edge("budget_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", END)

    return graph.compile()