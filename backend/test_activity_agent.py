from app.agents.activity_agent import activity_agent


state = {
    "destination": "Singapore",
    "travelers": 2,
    "days": 5,
    "preferences": "sightseeing and food",
}


result = activity_agent(state)


print("\n================ ACTIVITY AGENT RESULT ================\n")

activities = result.get("activity_options", [])

print(f"Number of activities: {len(activities)}\n")

for i, activity in enumerate(activities, start=1):

    print(f"Activity {i}")
    print(f"Name: {activity.get('name')}")
    print(f"Description: {activity.get('description')}")
    print(
        f"Price per person: "
        f"{activity.get('price_per_person')} "
        f"{activity.get('currency')}"
    )
    print(f"Location: {activity.get('location')}")
    print(f"Link: {activity.get('link')}")
    print(f"Live API: {activity.get('live_api')}")
    print("-" * 60)