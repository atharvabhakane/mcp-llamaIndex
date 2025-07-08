import os
from dotenv import load_dotenv
from typing import Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Load secrets from .env
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

# MCP server instance
mcp = FastMCP("weatherapi")

BASE_URL = "http://api.weatherapi.com/v1"

# ----------------------------
# Tool 1: Get Weather by City
# ----------------------------

@mcp.tool()
async def get_weather(location: str) -> dict:
    """Get current weather info for a given city or region.

    Args:
        location: City or place name (e.g. Delhi, London)
    """
    if not API_KEY:
        return {"error": "API key is missing. Set WEATHER_API_KEY in .env"}

    url = f"{BASE_URL}/current.json?key={API_KEY}&q={location}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=20.0)
            response.raise_for_status()
            data = response.json()

        # Structure the response
        return {
            "location": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"]
        }

    except httpx.HTTPStatusError as http_err:
        return {"error": f"WeatherAPI error: {http_err.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# ----------------------------
# Run the server
# ----------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
