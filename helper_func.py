import json
# helper_func.py
import re

def clean_itinerary(text: str) -> str:
    """Clean LLM output into Markdown-friendly itinerary."""
    # Remove weird line breaks and multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Ensure Days are headers
    text = re.sub(r"(Day\s*\d+)", r"\n\n### \1", text)

    # Normalize activity labels
    text = text.replace("Morning:", "\n- **Morning:**")
    text = text.replace("Afternoon:", "\n- **Afternoon:**")
    text = text.replace("Evening:", "\n- **Evening:**")

    # Normalize costs
    text = re.sub(r"Total cost[:\s]*\$?(\d+)", r"\n💰 **Total cost:** $\1", text)

    return text.strip()




def clean_weather(raw_weather: str) -> str:
    try:
        # Ensure it's a dict
        if isinstance(raw_weather, str):
            weather = json.loads(raw_weather.replace("'", '"'))
        else:
            weather = raw_weather

        loc = weather["location"]["name"]
        cond = weather["current"]["condition"]["text"]
        temp = weather["current"]["temp_c"]
        feels = weather["current"]["feelslike_c"]
        wind = weather["current"]["wind_kph"]

        return f"Weather in {loc}: {cond}, {temp}°C (feels like {feels}°C), wind {wind} km/h."
    except Exception as e:
        return f"Could not parse weather: {e}"
