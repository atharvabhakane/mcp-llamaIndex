from mcp.server.fastmcp import FastMCP
from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
import base64
from typing import List, Optional
import tempfile
import google.generativeai as genai
import traceback

# Load API keys from .env
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

mcp = FastMCP("llamaparse-idp-markdown")

def get_pdf_path(pdf_path: Optional[str], pdf_base64: Optional[str]) -> Optional[str]:
    if pdf_path and os.path.exists(pdf_path):
        return pdf_path
    elif pdf_base64:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(base64.b64decode(pdf_base64))
            return tmp.name
    return None

@mcp.tool()
async def extract_entities_2(entities: List[str], pdf_path: Optional[str] = None, pdf_base64: Optional[str] = None) -> dict:
    path = get_pdf_path(pdf_path, pdf_base64)
    if not path:
        return {"error": "❌ Provide a valid 'pdf_path' or 'pdf_base64'"}
    try:
        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="markdown", verbose=False)
        documents = parser.load_data(path)

        results = []
        for i, doc in enumerate(documents):
            page_entities = {}
            text = doc.text if hasattr(doc, "text") else ""

            # Use Gemini to normalize markdown output if configured
            if GEMINI_API_KEY:
                try:
                    model = genai.GenerativeModel("models/gemini-pro")
                    prompt = f"Clean and normalize this markdown:\n{text if text is not None else ''}"
                    response = model.generate_content(prompt)
                    text = response.text
                except Exception as gemini_error:
                    print(f"Gemini normalization failed: {gemini_error}")

            for entity in entities:
                found = False
                for line in text.splitlines():
                    if entity.lower() in line.lower():
                        clean_line = line.replace("**", "").strip()
                        parts = clean_line.split(":", 1)
                        if len(parts) == 2 and entity.lower() in parts[0].lower():
                            page_entities[entity] = parts[1].strip()
                            found = True
                            break
                        parts = clean_line.split("-", 1)
                        if len(parts) == 2 and entity.lower() in parts[0].lower():
                            page_entities[entity] = parts[1].strip()
                            found = True
                            break
                if not found:
                    page_entities[entity] = None
            results.append({"page": i + 1, "entities": page_entities})

        return {"pages": results}
    except Exception as e:
        return {"error": f"SDK parsing failed: {str(e)}\n{traceback.format_exc()}"}

@mcp.tool()
async def count_pages(pdf_path: Optional[str] = None, pdf_base64: Optional[str] = None) -> dict:
    path = get_pdf_path(pdf_path, pdf_base64)
    if not path:
        return {"error": "Provide a valid 'pdf_path' or 'pdf_base64'"}
    try:
        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="markdown", verbose=False)
        documents = parser.load_data(path)
        return {"total_pages": len(documents)}
    except Exception as e:
        return {"error": f"Failed to count pages: {str(e)}"}

@mcp.tool()
async def list_available_entities(pdf_path: Optional[str] = None, pdf_base64: Optional[str] = None) -> dict:
    path = get_pdf_path(pdf_path, pdf_base64)
    if not path:
        return {"error": "Provide a valid 'pdf_path' or 'pdf_base64'"}
    try:
        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="markdown", verbose=False)
        documents = parser.load_data(path)
        candidates = set()
        for doc in documents:
            text = doc.text if hasattr(doc, "text") else ""
            for line in text.splitlines():
                clean_line = line.replace("**", "").strip()
                if ':' in clean_line:
                    key = clean_line.split(':')[0].strip()
                    if key and len(key.split()) <= 4:
                        candidates.add(key)
        return {"detected_entity_names": sorted(candidates)}
    except Exception as e:
        return {"error": f"Failed to extract entity names: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
