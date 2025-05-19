import requests
import json

def main():
    print("🌤️  MCP Client - Weather Command (Level 2)")
    
    # Take location input from user
    location = input("Enter location to get current weather: ").strip()

    # Build request payload
    payload = {
        "command": "weather",
        "location": location
    }

    try:
        # Send POST request to MCP server (now on port 8001)
        response = requests.post("http://127.0.0.1:8001/mcp", json=payload)

        # Parse and print the response
        print("\n🌐 Response from MCP Server:")
        print(json.dumps(response.json(), indent=2))

    except requests.exceptions.RequestException as e:
        print("❌ Error connecting to MCP server:")
        print(str(e))

if __name__ == "__main__":
    main()
