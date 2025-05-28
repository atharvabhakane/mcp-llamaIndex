from mcp.server.fastmcp import FastMCP
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
import base64
import requests
from typing import List, Optional

# Load API key from .env
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
LLAMA_API_URL = "https://api.llamaparse.com/v1/extract"

# Initialize FastMCP server
mcp = FastMCP("llamaparse-idp-final")

# Helper function to get base64 from either source
def get_base64(pdf_path: Optional[str], pdf_base64: Optional[str]) -> dict:
    if pdf_base64:
        return {"content": pdf_base64, "name": "uploaded.pdf"}
    elif pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return {"content": encoded, "name": os.path.basename(pdf_path)}
    else:
        return {"error": "❌ Provide a valid 'pdf_path' or 'pdf_base64'"}

# ✅ Tool 1: Extract entities with per-page output
@mcp.tool()
async def extract_entities_2(
    entities: List[str], 
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    if not LLAMA_API_KEY:
        return {"error": "LlamaParse API key not configured"}

    data = get_base64(pdf_path, pdf_base64)
    if "error" in data:
        return data

    try:
        payload = {
            "document": {
                "content": data["content"],
                "name": data["name"]
            },
            "entities": entities
        }
        headers = {
            "Authorization": f"Bearer {LLAMA_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(LLAMA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "pages" in result:
            return result
        else:
            return {
                "pages": [
                    {
                        "page": 1,
                        "entities": result.get("entities", {})
                    }
                ]
            }

    except Exception as api_error:
        try:
            parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=False)
            documents = parser.load_data(pdf_path)

            if not documents or not hasattr(documents[0], "text"):
                return {"error": "Fallback parsing failed: no text extracted."}

            return {
                "note": "Fallback: full document text returned.",
                "pages": [
                    {
                        "page": i + 1,
                        "text": doc.text
                    } for i, doc in enumerate(documents)
                ]
            }
        except Exception as fallback_error:
            return {
                "error": "Both API and fallback extraction failed.",
                "api_error": str(api_error),
                "fallback_error": str(fallback_error)
            }

# ✅ Tool 2: Count number of pages in PDF
@mcp.tool()
async def count_pages(
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    data = get_base64(pdf_path, pdf_base64)
    if "error" in data:
        return data

    try:
        # Save temp file if base64
        if pdf_base64:
            with open("temp_count.pdf", "wb") as f:
                f.write(base64.b64decode(data["content"]))
            path = "temp_count.pdf"
        else:
            path = pdf_path

        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=False)
        documents = parser.load_data(path)
        return {"total_pages": len(documents)}
    except Exception as e:
        return {"error": f"Failed to count pages: {str(e)}"}

# ✅ Tool 3: Detect available entities from PDF text
@mcp.tool()
async def list_available_entities(
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    data = get_base64(pdf_path, pdf_base64)
    if "error" in data:
        return data

    try:
        # Save temp file if base64
        if pdf_base64:
            with open("temp_entities.pdf", "wb") as f:
                f.write(base64.b64decode(data["content"]))
            path = "temp_entities.pdf"
        else:
            path = pdf_path

        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=False)
        documents = parser.load_data(path)
        if not documents:
            return {"error": "No pages found in document."}

        candidates = set()
        for doc in documents:
            lines = doc.text.split("\n")
            for line in lines:
                if ':' in line:
                    key = line.split(':')[0].strip()
                    if key and len(key.split()) <= 4:
                        candidates.add(key)

        return {"detected_entity_names": sorted(candidates)}

    except Exception as e:
        return {"error": f"Failed to extract entity names: {str(e)}"}

# ✅ Run the MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
