# This file contains the implementation of the FastMCP server for document processing.
# It leverages LlamaParse for PDF parsing and extracts specified entities from the documents.

from __future__ import annotations

import os
import base64
import tempfile
import difflib
from typing import List, Optional

from dotenv import load_dotenv
from llama_parse import LlamaParse

from mcp.server.fastmcp import FastMCP

# Load API key (used by LlamaParse SDK) from environment variables.
# This ensures that sensitive information is not hardcoded and can be managed externally.
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

# Initialize FastMCP application with a service name.
mcp = FastMCP("server-sdk")

def get_pdf_path(pdf_path: Optional[str], pdf_base64: Optional[str]) -> Optional[str]:
    """
    Determines the PDF file path from either a direct path or a base64 encoded string.

    Args:
        pdf_path (Optional[str]): The direct file path to the PDF document.
        pdf_base64 (Optional[str]): The base64 encoded string of the PDF document.

    Returns:
        Optional[str]: The resolved PDF file path, or None if neither a valid path nor base64 is provided.
    """
    # If a direct path is provided and exists, use it.
    if pdf_path and os.path.exists(pdf_path):
        return pdf_path
    # If a base64 string is provided, decode it and save to a temporary file.
    elif pdf_base64:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(base64.b64decode(pdf_base64))
            return tmp.name
    # If neither is valid, return None.
    return None

@mcp.tool()
async def extract_entities(
    entities: List[str],
    pdf_path: Optional[str] = None,
    pdf_base64: Optional[str] = None
) -> dict:
    """
    Extracts specified entities from a PDF document.

    The PDF can be provided either as a file path or a base64 encoded string.
    It uses LlamaParse to process the document and then attempts to find entities
    by matching keys in the extracted text.

    Args:
        entities (List[str]): A list of entity names to extract.
        pdf_path (Optional[str]): The file path to the PDF document.
        pdf_base64 (Optional[str]): The base64 encoded string of the PDF document.

    Returns:
        dict: A dictionary containing the extracted entities per page, or an error message.
    """
    # Determine the actual PDF path from the provided arguments.
    path = get_pdf_path(pdf_path, pdf_base64)
    if not path:
        return {"error": "Provide a valid 'pdf_path' or 'pdf_base64'"}

    print("[INFO] SDK Parsing Started with Key:", LLAMA_API_KEY)

    try:
        # Initialize LlamaParse with the API key and desired result type.
        parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=False)
        # Load data from the PDF document.
        documents = parser.load_data(path)

        pages_result = []
        # Iterate through each page/document processed by LlamaParse.
        for i, doc in enumerate(documents):
            text = doc.text
            lines = text.splitlines()
            found = {}

            # For each entity, attempt to find its value in the document text.
            for entity in entities:
                best_match = None
                best_value = None
                best_ratio = 0.0

                # Search for the entity within each line of the document.
                for line in lines:
                    parts = []
                    # Split the line by common key-value delimiters.
                    if ':' in line:
                        parts = line.split(":", 1)
                    elif '-' in line:
                        parts = line.split("-", 1)
                    else:
                        continue

                    # If a key-value pair is found, compare the key with the target entity.
                    if len(parts) == 2:
                        key, value = parts[0].strip(), parts[1].strip()
                        # Use sequence matcher to find the best fuzzy match for the entity key.
                        ratio = difflib.SequenceMatcher(None, key.lower(), entity.lower()).ratio()
                        # Update best match if a better ratio is found.
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_match = key
                            best_value = value

                # If a sufficiently good match is found (ratio > 0.7), store the extracted value.
                if best_ratio > 0.7:
                    found[entity] = best_value
                else:
                    found[entity] = None  # Indicate that the entity was not found.

            # Append the extracted entities for the current page to the results.
            pages_result.append({
                "page": i + 1,
                "entities": found
            })

        return {"pages": pages_result}

    except Exception as e:
        # Catch any exceptions during parsing and return an error message.
        return {"error": f"SDK parsing failed: {str(e)}"}

# Entry point for running the FastMCP server.
# The server will listen for incoming requests to process documents.
if __name__ == "__main__":
    mcp.run(transport="http-streaming", host="127.0.0.1", port=8000)
