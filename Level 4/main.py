from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
import re
from llama_parse import LlamaParse

# Load API key from .env
load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

app = FastAPI()

# MCP request format
class MCPRequest(BaseModel):
    command: str
    document_path: Optional[str] = None
    entities: Optional[List[str]] = []

def extract_invoice_data(text: str) -> List[Dict]:
    """Extract and group invoice data from text."""
    # Find all invoice numbers first
    invoice_numbers = re.finditer(r"INV[- ]?\d+", text)
    invoices = []
    
    # Convert text to list of lines for easier processing
    lines = text.split('\n')
    
    for invoice_match in invoice_numbers:
        invoice_number = invoice_match.group()
        start_pos = invoice_match.start()
        
        # Get the section of text for this invoice
        # Look for the next invoice number or end of text
        next_invoice = re.search(r"INV[- ]?\d+", text[start_pos + len(invoice_number):])
        end_pos = start_pos + len(invoice_number) + next_invoice.start() if next_invoice else len(text)
        
        invoice_text = text[start_pos:end_pos]
        
        # Initialize entities with None values to maintain order
        entities = {
            "invoice_number": None,
            "date": None,
            "customer": None,
            "total": None
        }
        
        # Extract invoice number
        entities["invoice_number"] = invoice_number
        
        # Extract date - look for date in multiple formats
        date_patterns = [
            r"\d{4}-\d{2}-\d{2}",  # YYYY-MM-DD
            r"\d{2}/\d{2}/\d{4}",  # MM/DD/YYYY
            r"\d{2}-\d{2}-\d{4}"   # DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, invoice_text)
            if date_match:
                entities["date"] = date_match.group()
                break
        
        # Extract customer - look for customer information in multiple formats
        customer_patterns = [
            r"(?:Customer|Billed To|Client|To|Bill To)[:\- ]+\s*([A-Za-z\s]+(?:[A-Za-z\s]+)*)",
            r"(?:Customer|Billed To|Client|To|Bill To)[:\- ]+\s*([A-Za-z\s]+(?:[A-Za-z\s]+)*)(?:\n|$)",
            r"(?:Customer|Billed To|Client|To|Bill To)[:\- ]+\s*([A-Za-z\s]+(?:[A-Za-z\s]+)*)(?:,|$)"
        ]
        
        for pattern in customer_patterns:
            customer_match = re.search(pattern, invoice_text, re.IGNORECASE)
            if customer_match:
                customer_name = customer_match.group(1).strip()
                # Clean up the customer name
                customer_name = re.sub(r'\s+', ' ', customer_name)  # Remove extra spaces
                customer_name = customer_name.split('\n')[0]  # Take only first line
                customer_name = customer_name.split(',')[0]  # Remove anything after comma
                entities["customer"] = customer_name.strip()
                break
        
        # Extract total - look for total in multiple formats
        total_patterns = [
            r"\$\d+(?:,\d{3})*(?:\.\d{2})?",  # $1,234.56
            r"Total:?\s*\$?\d+(?:,\d{3})*(?:\.\d{2})?",  # Total: $1,234.56
            r"Amount:?\s*\$?\d+(?:,\d{3})*(?:\.\d{2})?"   # Amount: $1,234.56
        ]
        
        for pattern in total_patterns:
            total_match = re.search(pattern, invoice_text)
            if total_match:
                total = total_match.group()
                # Clean up the total value
                total = re.sub(r'[^\d.,$]', '', total)  # Remove non-numeric characters except $, ., and ,
                if not total.startswith('$'):
                    total = '$' + total
                entities["total"] = total
                break
        
        # Only add invoice if it has at least invoice number and one other field
        if entities["invoice_number"] and any(v for k, v in entities.items() if k != "invoice_number" and v is not None):
            invoices.append(entities)
    
    return invoices

# Endpoint to handle MCP requests
@app.post("/mcp")
async def handle_mcp(request: MCPRequest):
    if request.command.lower() == "extract":
        if not request.document_path or not request.entities:
            return {"error": "Both 'document_path' and 'entities' are required for extract command."}

        # Check if file exists
        if not os.path.exists(request.document_path):
            return {"error": f"File not found: {request.document_path}"}

        try:
            # Initialize LlamaParse
            parser = LlamaParse(api_key=LLAMA_API_KEY, result_type="text", verbose=True)
            print("Successfully initialized LlamaParse!")
            
            # Process the PDF file
            print(f"Processing {request.document_path}...")
            documents = parser.load_data(request.document_path)
            
            if not documents:
                return {"error": "No documents were returned from the parser"}
            
            all_invoices = []
            for i, doc in enumerate(documents):
                if not hasattr(doc, 'text') or not doc.text:
                    continue

                # Print the extracted text for debugging
                print(f"\nExtracted text from Page {i+1}:")
                print("-" * 50)
                print(doc.text)
                print("-" * 50)

                # Extract and group invoice data
                page_invoices = extract_invoice_data(doc.text)
                all_invoices.extend(page_invoices)

            if not all_invoices:
                return {"error": "No invoices found in the document"}

            return {"invoices": all_invoices}

        except Exception as e:
            print(f"Error details: {str(e)}")  # Print error details to server console
            return {"error": f"Failed to process document: {str(e)}"}

    return {"error": f"Unsupported command: {request.command}"}