import streamlit as st
from workflow import app

st.set_page_config(page_title="Travel Planner AI", page_icon="🌍", layout="wide")

st.title("🌍 AI Travel Planner")
st.write("Plan your trip with an AI-powered itinerary generator.")

# --- Input Form ---
with st.form("travel_form"):
    destination = st.text_input("Destination", "Paris")
    budget = st.number_input("Budget (USD)", min_value=100, value=1000, step=50)
    interests = st.multiselect(
        "Interests",
        ["art", "food", "history", "nature", "adventure", "shopping", "beach"],
        default=["art", "food"]
    )
    dates = st.text_input("Travel Dates (YYYY-MM-DD to YYYY-MM-DD)", "2025-10-01 to 2025-10-03")
    submitted = st.form_submit_button("Generate Itinerary")

# --- Processing ---
if submitted:
    with st.spinner("Planning your trip... ✈️"):
        preferences = {
            "destination": destination,
            "budget": budget,
            "interests": interests,
            "dates": dates
        }
        try:
            result = app.invoke({"preferences": preferences})
            itinerary = result.get("itinerary", "No itinerary generated.")
            weather = result.get("weather", "No weather data available.")

            # --- Output Display ---
            st.subheader("📅 Itinerary")
            st.write(itinerary)

            st.subheader("🌦️ Weather Forecast")
            st.write(weather)

        except Exception as e:
            st.error(f"An error occurred: {e}")
