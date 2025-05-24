from mcp.server.fastmcp import FastMCP
import re

# Initialize FastMCP server
mcp = FastMCP("simulated-idp")

@mcp.tool()
async def extract(document: str, entities: list[str]) -> dict:
    """
    Simulate entity extraction from a document string.

    Args:
        document: The raw text of a document.
        entities: A list of entity names to extract (any kind).
    """
    extracted = {}
    messages = []

    # Split document into lines
    lines = document.split("\n")

    for entity in entities:
        entity_clean = entity.strip().lower()
        found = False

        for line in lines:
            line_lower = line.lower()
            if entity_clean in line_lower:
                # Look for patterns like "entity: value" or "entity - value"
                match = re.search(rf"{entity_clean}\s*[:\-]\s*(.+)", line, re.IGNORECASE)
                value = match.group(1).strip() if match else line.strip()
                extracted[entity] = value
                found = True
                break

        if not found:
            messages.append(
                f"I couldn’t extract \"{entity}\" — it’s not found in the document."
            )

    return {
        "pages": [
            {
                "page": 1,
                "entities": extracted,
                "messages": messages
            }
        ]
    }

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
