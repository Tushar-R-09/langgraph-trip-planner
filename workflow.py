# workflow.py
from langgraph.graph import StateGraph, END
from tavily import TavilyClient
from typing import TypedDict
from datetime import datetime
import os
from dotenv import load_dotenv

from llm import llm  # our TinyLlama-based LLM function

# Load environment variables
load_dotenv()

# Tavily API client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Define the state structure
class TravelPlanState(TypedDict):
    preferences: dict
    destination_info: str
    itinerary: str
    weather: str


# Step 1: Gather preferences
def gather_preferences(state: TravelPlanState):
    return {"preferences": state["preferences"]}


# Step 2: Fetch destination info
def fetch_destination_info(state: TravelPlanState):
    query = (
        f"Top attractions and activities in {state['preferences']['destination']} "
        f"for {state['preferences']['interests']}"
    )
    info = tavily.search(query=query, max_results=2)

    # Merge results into a short paragraph
    combined_info = " ".join(result["content"] for result in info.get("results", []))
    return {"destination_info": combined_info[:500]}  # limit size


# Step 3: Generate itinerary with LLM
def generate_itinerary(state: TravelPlanState):
    # Calculate trip days
    dates = state['preferences'].get('dates', "")
    try:
        start_date, end_date = dates.split(" to ")
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end - start).days + 1
    except (ValueError, AttributeError):
        num_days = 5  # fallback

    # Build prompt
    prompt = (
        f"You are a travel planner AI.\n"
        f"Generate a detailed {num_days}-day travel itinerary for {state['preferences']['destination']}.\n"
        f"Total budget: ${state['preferences']['budget']}.\n"
        f"Traveler interests: {', '.join(state['preferences']['interests'])}.\n"
        f"Reference information: {state['destination_info']}.\n"
        f"Output format:\n"
        f"- Day X: Morning activity (cost), Afternoon activity (cost), Evening activity (cost)\n"
        f"- End each day with the total cost for that day.\n"
        f"- Ensure the overall cost is within budget.\n"
        f"Do not explain the format, only provide the itinerary."
    )


    # Call local LLM
    raw_output = llm(prompt)

    # Extract itinerary text
    return {"itinerary": raw_output.strip()}


# Step 4: Fetch weather
def check_weather(state: TravelPlanState):
    query = (
        f"Weather forecast for {state['preferences']['destination']} "
        f"on {state['preferences']['dates']}"
    )
    weather_data = tavily.search(query=query, max_results=1)
    weather_text = weather_data["results"][0]["content"] if weather_data.get("results") else "No weather data found."
    return {"weather": weather_text}


# Build the workflow graph
workflow = StateGraph(TravelPlanState)
workflow.add_node("gather_preferences", gather_preferences)
workflow.add_node("fetch_info", fetch_destination_info)
workflow.add_node("generate_itinerary", generate_itinerary)
workflow.add_node("check_weather", check_weather)

# Define flow
workflow.add_edge("gather_preferences", "fetch_info")
workflow.add_edge("fetch_info", "generate_itinerary")
workflow.add_edge("generate_itinerary", "check_weather")

# Entry and exit
workflow.set_entry_point("gather_preferences")
workflow.add_edge("check_weather", END)

# Compile app
app = workflow.compile()
