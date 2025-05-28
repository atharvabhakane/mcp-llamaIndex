from mcp.server.fastmcp import FastMCP
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
import requests
import base64
from typing import List, Optional
import sys
import codecs
import locale

# ----------------- Encoding Setup -----------------
def setup_encoding():
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            pass
    os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
    os.environ['PYTHONLEGACYWINDOWSSTDIO'] = '1'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach(), errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    else:
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach(), errors='replace')

setup_encoding()

# ----------------- Environment Setup -----------------
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
LLAMA_API_URL = "https://api.llamaparse.com/v1/extract"

mcp = FastMCP("llamaparse-level4")

# ----------------- Helper Function -----------------
def get_base64(pdf_path: Optional[str], pdf_base64: Optional[str]) -> Optional[str]:
    if pdf_base64:
        return pdf_base64
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

# ----------------- Extraction Tool -----------------
@mcp.tool()
async def extract_entities(pdf_path: Optional[str] = None, pdf_base64: Optional[str] = None, entities: List[str] = []) -> dict:
    if not entities:
        return {"error": "Entities list is required"}
    if not LLAMA_API_KEY:
        return {"error": "API key is not set"}
    
    encoded = get_base64(pdf_path, pdf_base64)
    if not encoded:
        return {"error": "❌ Provide a valid 'pdf_path' or 'pdf_base64'"}

    try:
        payload = {
            "document": {
                "content": encoded,
                "name": os.path.basename(pdf_path) if pdf_path else "document.pdf"
            },
            "entities": entities
        }
        headers = {
            "Authorization": f"Bearer {LLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as api_error:
        return {
            "error": f"API call failed: {str(api_error)}"
        }

# ----------------- Health Check Tool -----------------
@mcp.tool()
async def test_connection() -> dict:
    return {
        "status": "connected",
        "api_key_present": bool(LLAMA_API_KEY),
        "transport": "stdio"
    }

# ----------------- Run Server -----------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
