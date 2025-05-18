# MCP Entity Extraction System

A simple and efficient system for extracting key information from documents using FastAPI and Python.

## 🚀 Overview

This project helps you extract important information (like invoice numbers, customer names, dates, and totals) from text documents. It consists of two main parts:
- A FastAPI server that processes the documents
- A simple command-line client to interact with the server

## 📋 Prerequisites

Before you begin, make sure you have:
- Python 3.7 or higher installed
- Basic understanding of command-line operations

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install the required packages:
```bash
pip install fastapi uvicorn requests
```

## 🏃‍♂️ How to Run

### Step 1: Start the Server
Open a terminal and run:
```bash
uvicorn main:app --reload
```
You should see output indicating the server is running, typically at `http://127.0.0.1:8000`

### Step 2: Run the Client
Open another terminal and run:
```bash
python client.py
```

## 🔄 How It Works

Here's a simple flow chart showing how the system works:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    You      │     │   Client    │     │   Server    │
│  (User)     │     │  (client.py)│     │ (main.py)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ 1. Enter         │                   │
       │    Document      │                   │
       │    & Entities    │                   │
       │─────────────────>│                   │
       │                   │                   │
       │                   │ 2. Send Request   │
       │                   │    to Server      │
       │                   │──────────────────>│
       │                   │                   │
       │                   │                   │ 3. Process
       │                   │                   │    Document
       │                   │                   │
       │                   │                   │ 4. Extract
       │                   │                   │    Information
       │                   │                   │
       │                   │ 5. Send Results   │
       │                   │<──────────────────│
       │                   │                   │
       │ 6. See Results    │                   │
       │<─────────────────│                   │
       │                   │                   │
```

## 📝 Example Usage

1. When you run the client, you'll be asked to enter:
   - The document text (in a single line)
   - The entities you want to extract (comma-separated)

2. Example input:
```
Enter document text (single line):
> Invoice No: INV-12345 Customer: John Doe Date: 2024-06-01 Total: $100.00

Enter entities to extract (comma-separated):
> invoice_number, customer, date, total
```

3. Example output:
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

## 📁 Project Structure

```
.
├── main.py      # FastAPI server code
├── client.py    # Command-line client
└── README.md    # This documentation
```

## ⚠️ Important Notes

1. Always start the server before running the client
2. The server must be running at `http://127.0.0.1:8000`
3. The system works best with well-formatted text documents
4. Supported entities include:
   - invoice_number
   - customer
   - date
   - total

## 🆘 Troubleshooting

If you encounter any issues:
1. Make sure the server is running
2. Check that you're using Python 3.7 or higher
3. Verify all required packages are installed
4. Ensure your document text is properly formatted

## 🤝 Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## 📄 License

This project is open source and available under the MIT License. 