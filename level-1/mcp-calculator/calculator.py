from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("calculator")

@mcp.tool()
async def add(numbers: list[float]) -> float:
    """Add a list of numbers together.

    Args:
        numbers: List of numbers to add
    """
    return sum(numbers)

@mcp.tool()
async def subtract(numbers: list[float]) -> float:
    """Subtract a list of numbers in order (left to right).

    Args:
        numbers: List of numbers to subtract
    """
    if len(numbers) < 2:
        raise ValueError("Need at least two numbers to subtract.")
    
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

@mcp.tool()
async def hello(name: str) -> str:
    """Greet someone by name.
    
    Args:
        name: Name of the person to greet
    """
    return f"Hello, {name}! Welcome to the MCP add, sub, and hello server!"

if __name__ == "__main__":
    # Run the MCP server using STDIO
    mcp.run(transport='stdio')
