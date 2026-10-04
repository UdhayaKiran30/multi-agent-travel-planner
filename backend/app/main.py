from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.graph.travel_graph import build_travel_graph


app = FastAPI(
    title="Multi-Agent Travel Planner",
    description="AI-powered multi-agent travel planning system",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


travel_graph = build_travel_graph()


class TravelRequest(BaseModel):
    request: str


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Travel Planner API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/plan")
def create_travel_plan(request: TravelRequest):

    initial_state = {
        "user_request": request.request,

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

    result = travel_graph.invoke(initial_state)

    return {
    "travel_details": {
        "origin": result["origin"],
        "destination": result["destination"],
        "days": result["days"],
        "travelers": result["travelers"],
        "budget": result["budget"],
        "preferences": result["preferences"],
    },
    
    "flight_options": result["flight_options"],
    "hotel_options": result["hotel_options"],
    "activity_options": result["activity_options"],

    "budget_analysis": result["budget_analysis"],

    "itinerary": result["itinerary"],
}