from app.agents.hotel_agent import hotel_agent


state = {
    "destination": "Singapore",
    "travelers": 2,
    "days": 5,
    "departure_date": "2026-10-15",
    "return_date": "2026-10-19",
}


result = hotel_agent(state)


print("\n================ HOTEL AGENT RESULT ================\n")

hotels = result.get("hotel_options", [])

print(f"Number of hotels: {len(hotels)}\n")

for i, hotel in enumerate(hotels, start=1):

    print(f"Hotel {i}")
    print(f"Name: {hotel.get('name')}")
    print(f"Price per night: ₹{hotel.get('price_per_night')}")
    print(f"Total price: ₹{hotel.get('total_price')}")
    print(f"Rating: {hotel.get('rating')}")
    print(f"Reviews: {hotel.get('reviews')}")
    print(f"Amenities: {hotel.get('amenities')}")
    print(f"Live API: {hotel.get('live_api')}")
    print("-" * 50)