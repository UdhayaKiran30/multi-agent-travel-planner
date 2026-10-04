from app.graph.travel_graph import build_travel_graph

graph = build_travel_graph()

initial_state = {
    "user_request": """
    I want to travel from Chennai to Singapore
    for 5 days with 2 travelers.
    My budget is 80000 rupees.
    I like sightseeing and food.
    Travel dates are October 15, 2026 to October 19, 2026.
    """,

    "origin": "",
    "origin_airport": "",

    "destination": "",
    "destination_airport": "",

    "days": 0,
    "travelers": 0,
    "budget": 0,
    "preferences": "",

    "departure_date": "",
    "return_date": "",

    "flight_options": [],
    "hotel_options": [],
    "activity_options": [],

    "budget_analysis": {},
    "itinerary": {},
}

result = graph.invoke(initial_state)

print("\n==============================")
print("FLIGHT OPTIONS")
print("==============================")

for i, flight in enumerate(result["flight_options"], 1):
    print(f"\nFlight {i}")
    print("Airline:", flight["airline"])
    print("Price:", flight["total_price"])
    print("Outbound:", flight["outbound"]["route"])
    print("Departure:", flight["outbound"]["departure_time"])
    print("Arrival:", flight["outbound"]["arrival_time"])
    print("Return:", flight["return"]["route"])
    print("Return Departure:", flight["return"]["departure_time"])
    print("Return Arrival:", flight["return"]["arrival_time"])
    print("Source:", flight["source"])
    print("Live API:", flight["live_api"])

print("\n==============================")
print("TOTAL FLIGHTS:", len(result["flight_options"]))
print("==============================")

print("\n==============================")
print("BUDGET ANALYSIS")
print("==============================")

budget_analysis = result["budget_analysis"]

print("Flight Cost:", budget_analysis["flight_cost"])
print("Hotel Cost:", budget_analysis["hotel_cost"])
print("Activity Cost:", budget_analysis["activity_cost"])
print("Total Cost:", budget_analysis["total_cost"])
print("Budget:", budget_analysis["budget"])
print("Remaining Budget:", budget_analysis["remaining_budget"])
print("Within Budget:", budget_analysis["within_budget"])

print("\nSelected Flight:")
print(budget_analysis["selected_flight"])

print("\nSelected Hotel:")
print(budget_analysis["selected_hotel"])

print("\nSelected Activities:")
for activity in budget_analysis["selected_activities"]:
    print(activity)

print("\nReasoning:")
print(budget_analysis["reasoning"])

print("\nBudget Status:")
print(budget_analysis["budget_status"])