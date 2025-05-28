from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
class MCPRequest(BaseModel):
    command: str
    numbers: Optional[list[float]] = []

@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    command = request.command.lower()
    numbers = request.numbers or []

    if command == "add":
        result = sum(numbers)
    elif command == "subtract":
        if len(numbers) < 2:
            return {"error": "Need at least 2 numbers to subtract"}
        result = numbers[0]
        for num in numbers[1:]:
            result -= num
    elif command == "hello":
        return {"response": "Hello, MCP World!"}
    else:
        return {"error": f"Unknown command: {command}"}

    return {
        "command": command,
        "input": numbers,
        "result": result
    }


# Use Copilot to Generate Tests

# Example test function to call MCP /mcp endpoint with "add" command and numbers 1, 2, 3
# import requests

# def test_add_command():
#     url = "http://127.0.0.1:8000/mcp"
#     payload = {"command": "add", "numbers": [1, 2, 3]}
#     response = requests.post(url, json=payload)
#     print(response.json())

# Example test function to call MCP /mcp endpoint with "subtract" command and numbers 10, 4

# def test_subtract_command():
#     url = "http://127.0.0.1:8000/mcp"
#     payload = {"command": "subtract", "numbers": [10, 4]}
#     response = requests.post(url, json=payload)
#     print(response.json())

# The output of this testing will be printed to the console where you run this script.
# To see the output, run this file in your terminal or command prompt.
