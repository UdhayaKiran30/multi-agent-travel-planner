from app.tools.flight_tools import search_flights


result = search_flights.invoke({
    "origin": "MAA",
    "destination": "SIN",
    "travelers": 2,
    "departure_date": "2026-10-15",
    "return_date": "2026-10-19",
})

print(result)