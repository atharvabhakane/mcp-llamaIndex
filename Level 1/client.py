import requests
import json

def main():
    print("Welcome to MCP CLI")
    print("Available commands: add, subtract, hello")

    command = input("Enter command: ").strip()
    numbers = []

    if command in ["add", "subtract"]:
        nums = input("Enter numbers separated by space: ")
        numbers = [float(n) for n in nums.split()]

    payload = {
        "command": command,
        "numbers": numbers
    }

    try:
        response = requests.post("http://localhost:8000/mcp", json=payload)
        print("Response from MCP:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print("Failed to connect to MCP server:", e)

if __name__ == "__main__":
    main()

# Auto-complete a request function by Copilot

# def send_hello_request():
#     url = "http://localhost:8000/mcp"
#     payload = {
#         "command": "hello"
#     }
#     response = requests.post(url, json=payload)
#     print("Response from MCP:", response.json())

# def send_add_request():
#     url = "http://localhost:8000/mcp"
#     payload = {
#         "command": "add",
#         "numbers": [1, 2, 3]
#     }
#     response = requests.post(url, json=payload)
#     print("Response from MCP:", response.json())

# def send_subtract_request():
#     url = "http://localhost:8000/mcp"
#     payload = {
#         "command": "subtract",
#         "numbers": [10, 4]
#     }
#     response = requests.post(url, json=payload)
#     print("Response from MCP:", response.json())

# # Call the functions
# send_add_request()
# send_subtract_request()
