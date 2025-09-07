from typing import TypedDict
class TravelPlanState(TypedDict):
    preferences: dict  # e.g., {"destination": "Paris", "budget": 1000, "interests": ["art", "food"], "dates": "2025-10-01 to 2025-10-07"}
    destination_info: str
    itinerary: str
    weather: str