# Simulated IDP (Level 3) – MCP Entity Extraction

This project simulates an Intelligent Document Processing (IDP) system that extracts key entities from a document using a FastAPI backend and a simple Python client.

## Features

- **Entity Extraction**: Extracts entities like `invoice_number`, `customer`, `date`, and `total` from a text document.
- **REST API**: FastAPI backend exposes a `/mcp` endpoint for extraction.
- **Interactive Client**: Command-line client to interact with the backend.

---

## Project Structure

```
.
├── main.py      # FastAPI backend (MCP server)
├── client.py    # Command-line client
└── __pycache__/ # Python cache files
```

---

## How It Works

### 1. Start the MCP Server

Run the backend server:
```bash
uvicorn main:app --reload
```

### 2. Run the Client

In a new terminal, run:
```bash
python client.py
```

### 3. Extraction Flow

- The client prompts you to enter document text and entities to extract.
- It sends a POST request to the `/mcp` endpoint.
- The server extracts the requested entities using regex patterns.
- The client displays the extracted entities.

---

## Flowchart

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │     │   Client    │     │   Server    │
│  (CLI App)  │     │  (client.py)│     │ (main.py)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ 1. Enter         │                   │
       │    Document      │                   │
       │    & Entities    │                   │
       │─────────────────>│                   │
       │                   │                   │
       │                   │ 2. POST Request   │
       │                   │    to /mcp        │
       │                   │──────────────────>│
       │                   │                   │
       │                   │                   │ 3. Process
       │                   │                   │    Document
       │                   │                   │
       │                   │                   │ 4. Extract
       │                   │                   │    Entities
       │                   │                   │
       │                   │ 5. JSON Response  │
       │                   │<──────────────────│
       │                   │                   │
       │ 6. Display        │                   │
       │    Results        │                   │
       │<─────────────────│                   │
       │                   │                   │
```

---

## Example

**Input:**
```
Enter document text (single line):
> Invoice No: INV-12345 Customer: John Doe Date: 2024-06-01 Total: $100.00

Enter entities to extract (comma-separated):
> invoice_number, customer, date, total
```

**Output:**
```json
{
  "pages": [
    {
      "page": 1,
      "entities": {
        "invoice_number": "INV-12345",
        "customer": "John Doe",
        "date": "2024-06-01",
        "total": "$100.00"
      }
    }
  ]
}
```

---

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Requests

Install dependencies:
```bash
pip install fastapi uvicorn requests
```

---

## Notes

- The extraction logic is simulated using regex and works for simple, well-formatted documents.
- The server must be running before starting the client. 