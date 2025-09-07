# run.py
from workflow import app

preferences = {
    "destination": "Paris",
    "budget": 1000,
    "interests": ["art", "food"],
    "dates": "2025-10-01 to 2025-10-03"
}
result = app.invoke({"preferences": preferences})
print("Itinerary:\n", result["itinerary"])
print("Weather:\n", result["weather"])