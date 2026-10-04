from app.graph.travel_graph import build_travel_graph


graph = build_travel_graph()


user_request = """
Plan a 5-day trip from Chennai to Singapore
for 2 people with a budget of ₹80,000.

Travel dates:
15 October 2026 to 19 October 2026.

Preferences:
sightseeing and food.
"""


initial_state = {
    "user_request": user_request,

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


print("\n================ FULL GRAPH RESULT ================\n")


print("ORIGIN:", result["origin"])
print("DESTINATION:", result["destination"])
print("DAYS:", result["days"])
print("TRAVELERS:", result["travelers"])
print("BUDGET:", result["budget"])

print("\n--------------------------------------------------")
print("FLIGHTS:", len(result["flight_options"]))

print("\n--------------------------------------------------")
print("HOTELS:", len(result["hotel_options"]))

print("\n--------------------------------------------------")
print("ACTIVITIES:", len(result["activity_options"]))

print("\n--------------------------------------------------")
print("BUDGET ANALYSIS")

budget = result["budget_analysis"]

print("Flight Cost:", budget.get("flight_cost"))
print("Hotel Cost:", budget.get("hotel_cost"))
print("Activity Cost:", budget.get("activity_cost"))
print("Total Cost:", budget.get("total_cost"))
print("Budget:", budget.get("budget"))
print("Remaining:", budget.get("remaining_budget"))
print("Within Budget:", budget.get("within_budget"))

print("\n--------------------------------------------------")
print("ITINERARY")

print(result["itinerary"])