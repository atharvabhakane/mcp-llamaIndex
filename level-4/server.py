from mcp.server.fastmcp import FastMCP
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
import requests
import base64
from typing import List
import sys
import html
import json
import logging
import codecs
import locale

# Critical: Set up encoding before any imports or operations
def setup_encoding():
    """Force UTF-8 encoding across the entire system"""
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

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
LLAMA_API_URL = "https://api.llamaparse.com/v1/extract"

mcp = FastMCP("llamaparse-dynamic")

def ascii_safe_print(message):
    try:
        safe_message = str(message).encode('ascii', errors='replace').decode('ascii')
        print(safe_message, flush=True)
    except Exception:
        print("Message contains non-printable characters", flush=True)

def ultra_sanitize_text(text):
    if not text:
        return ""
    try:
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='replace')
        sanitized = ""
        for char in str(text):
            if ord(char) < 128 or char in ['\n', '\r', '\t']:
                sanitized += char
            else:
                sanitized += '?'  # Replace with safe character
        return sanitized
    except Exception:
        return "[TEXT CONTENT - ENCODING ISSUES PREVENTED DISPLAY]"

def extract_simple_entities(text, entities):
    results = {}
    try:
        safe_text = ultra_sanitize_text(text)
        lines = safe_text.split('\n')
        for entity in entities:
            entity_safe = ultra_sanitize_text(entity.lower())
            results[entity] = []
            for i, line in enumerate(lines):
                line_safe = ultra_sanitize_text(line.lower())
                if entity_safe in line_safe:
                    if ':' in line:
                        parts = line.split(':', 1)
                        value = parts[1].strip()[:100] if len(parts) > 1 else line.strip()[:100]
                    else:
                        words = line.split()
                        value = next((word for word in words if any(c.isdigit() for c in word)), line.strip()[:100])
                    if value:
                        results[entity].append({
                            "value": ultra_sanitize_text(value),
                            "line": i + 1,
                            "found_in": ultra_sanitize_text(line.strip()[:200])
                        })
        return results
    except Exception as e:
        ascii_safe_print(f"Entity extraction error: {str(e)}")
        return {entity: [] for entity in entities}

@mcp.tool()
async def extract_entities(pdf_path: str, entities: List[str]) -> dict:
    if not pdf_path:
        return {"error": "PDF path required"}
    if not entities:
        return {"error": "Entities list required"}
    if not os.path.exists(pdf_path):
        return {"error": f"File not found: {pdf_path}"}
    if not LLAMA_API_KEY:
        return {"error": "API key not configured"}

    ascii_safe_print("Processing PDF file...")
    ascii_safe_print(f"Extracting: {', '.join(entities)}")

    try:
        ascii_safe_print("Attempting API extraction...")
        with open(pdf_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")

        payload = {
            "document": {"content": encoded, "name": os.path.basename(pdf_path)},
            "entities": entities
        }
        headers = {"Authorization": f"Bearer {LLAMA_API_KEY}", "Content-Type": "application/json"}

        response = requests.post(LLAMA_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            ascii_safe_print(f"API failed with status: {response.status_code}")
    except Exception as e:
        ascii_safe_print(f"API error: {str(e)[:100]}")

    ascii_safe_print("Using fallback parsing...")
    try:
        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=False)
        documents = parser.load_data(pdf_path)
        if not documents or not hasattr(documents[0], "text"):
            return {"error": "No text extracted from PDF"}

        raw_text = documents[0].text or ""
        safe_text = ultra_sanitize_text(raw_text)

        if not safe_text.strip():
            return {"error": "PDF appears to be empty"}

        extracted = extract_simple_entities(safe_text, entities)

        try:
            with open("debug_safe.txt", "w", encoding="ascii", errors="replace") as f:
                f.write(safe_text)
        except Exception:
            pass

        return {
            "status": "success_fallback",
            "method": "full_text_parse",
            "entities_found": extracted,
            "text_preview": safe_text[:500] + "..." if len(safe_text) > 500 else safe_text,
            "total_characters": len(safe_text)
        }
    except Exception as e:
        return {"error": f"Parsing failed: {str(e)[:200]}"}

@mcp.tool()
async def test_connection() -> dict:
    try:
        return {
            "status": "connected",
            "encoding": "ascii-safe",
            "api_key_present": bool(LLAMA_API_KEY),
            "test_message": "Server is working correctly"
        }
    except Exception as e:
        return {"error": f"Connection test failed: {str(e)}"}

if __name__ == "__main__":
    try:
        ascii_safe_print("Starting LlamaParse MCP Server (Encoding-Safe Version)...")
        ascii_safe_print(f"API Key Present: {bool(LLAMA_API_KEY)}")
        mcp.run(transport="stdio")
    except Exception as e:
        ascii_safe_print(f"Startup failed: {str(e)}")
        sys.exit(1)