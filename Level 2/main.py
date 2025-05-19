from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

# Define expected request body
class MCPRequest(BaseModel):
    command: str
    location: Optional[str] = None

@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    command = request.command.lower()

    if command == "weather":
        if not request.location:
            return {"error": "Location is required for weather command"}

        try:
            response = requests.get(
                "http://api.weatherapi.com/v1/current.json",
                params={"key": WEATHER_API_KEY, "q": request.location}
            )
            data = response.json()

            # Check for API errors
            if response.status_code != 200 or "error" in data:
                message = data.get("error", {}).get("message", "Unknown error")
                return {"error": f"WeatherAPI error: {message}"}

            # Return clean structured weather info
            return {
                "location": data["location"]["name"],
                "country": data["location"]["country"],
                "temperature_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"]
            }

        except Exception as e:
            return {"error": f"Failed to fetch weather: {str(e)}"}

    return {"error": "Only 'weather' command is supported in Level 2"}
