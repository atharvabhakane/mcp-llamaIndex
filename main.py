from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import re

app = FastAPI()

# ✅ Request format
class MCPRequest(BaseModel):
    command: str
    document: Optional[str] = None
    entities: Optional[List[str]] = []

# ✅ Simulated extraction logic
def simulate_extraction(document: str, entity_list: List[str]) -> dict:
    page_entities = {}

    # Simulated pattern-based extraction
    if "invoice_number" in entity_list:
        match = re.search(r"Invoice No[:\- ]+\s*(INV-\d+)", document)
        if match:
            page_entities["invoice_number"] = match.group(1)

    if "customer" in entity_list:
        match = re.search(r"Customer[:\- ]+\s*([A-Za-z\s]+)", document)
        if match:
            page_entities["customer"] = match.group(1).strip()

    if "date" in entity_list:
        match = re.search(r"Date[:\- ]+\s*(\d{4}-\d{2}-\d{2})", document)
        if match:
            page_entities["date"] = match.group(1)

    if "total" in entity_list:
        match = re.search(r"Total[:\- ]+\s*(\$[0-9]+(?:\.[0-9]{2})?)", document)
        if match:
            page_entities["total"] = match.group(1)

    return {
        "pages": [
            {
                "page": 1,
                "entities": page_entities
            }
        ]
    }

# ✅ MCP Endpoint
@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    if request.command.lower() == "extract":
        if not request.document or not request.entities:
            return {"error": "Document and entities list are required for 'extract' command"}
        return simulate_extraction(request.document, request.entities)

    return {"error": f"Unsupported command: {request.command}"}
