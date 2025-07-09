# MCP Entity Extraction System

A simple and efficient system for extracting key information from documents using FastMCP and Python.

## 🚀 Overview

This project helps you extract important information (like invoice numbers, customer names, dates, and totals) from text documents. It consists of a single Python script that processes the documents.

## 📋 Prerequisites

Before you begin, make sure you have:
- Python 3.7 or higher installed
- Basic understanding of command-line operations
- The necessary libraries for FastMCP installed (you may need to install `mcp`)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/atharvabhakane/MCP-Llama-parse.git
cd MCP-Llama-parse
```

2. Install the required packages:
```bash
pip install mcp
```

## 🏃‍♂️ How to Run

Open a terminal in the project directory and run:
```bash
python simulated_idp.py
```
The script will start and wait for input via standard input.

## 🔄 How It Works

Here's a simple flow chart showing how the system works:

```
┌─────────────┐     ┌─────────────────┐
│    You      │     │ simulated_idp.py│
│  (User)     │     │  (Script)       │
└──────┬──────┘     └──────┬──────────┘
       │                   │
       │ 1. Provide        │
       │    Document &     │
       │    Entities via   │
       │    Standard Input │
       │──────────────────>│
       │                   │
       │                   │ 2. Process
       │                   │    Document
       │                   │
       │                   │ 3. Extract
       │                   │    Information
       │                   │
       │ 4. See Results    │
       │    on Standard    │
       │    Output         │
       │<──────────────────│
       │                   │
```

## 📝 Example Usage

1. When you run the `simulated_idp.py` script, it will wait for input.
2. You will need to provide the document text and entities via standard input, likely in a format the script expects (based on the code, it seems to expect `document` and `entities` parameters, which would typically come from an MCP client, but for stdio, the format might need clarification). *Note: The exact input format for stdio transport is not clear from the code snippet. You may need to consult FastMCP documentation or experiment.*
3. Example of potential interaction (this is an illustrative example based on typical command-line interaction, the exact format depends on the FastMCP stdio implementation):
```bash
python simulated_idp.py
# Script is running, now provide input, e.g., as JSON
{"document": "Invoice No: INV-12345 Customer: John Doe Date: 2024-06-01 Total: $100.00", "entities": ["invoice_number", "customer", "date", "total"]}
```
4. The script will process the input and output the results to standard output.

Example output:
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
      },
      "messages": []
    }
  ]
}
```

---

## 🖼️ Visual Example: Entity Extraction

### Input Example

![Entity Extraction Input](../Images/Screenshot%202025-07-09%20203433.png)
* This shows the input invoice and the entity extraction request, specifying the entities to extract (Invoice No, Date, Status).* 

### Output Example

![Entity Extraction Output](../Images/Screenshot%202025-07-09%20203424.png)
* This shows the extracted output for the requested entities: invoice number, date, and status.*

## 📁 Project Structure

```
.
├── simulated_idp.py  # FastMCP script for entity extraction
└── README.md         # This documentation
```

## ⚠️ Important Notes

1. Run the `simulated_idp.py` script directly.
2. The script interacts via standard input and standard output. The exact input format expected by FastMCP's stdio transport may require further investigation.
3. The system works best with well-formatted text documents.
4. Supported entities are determined by the logic within the `extract` function (currently includes basic patterns for entities followed by ':' or '-').

## 🆘 Troubleshooting

If you encounter any issues:
1. Make sure the `mcp` library is installed (`pip install mcp`).
2. Check that you're using Python 3.7 or higher.
3. Ensure your document text is properly formatted for the script's extraction logic.
4. Verify the input format you are providing via standard input matches what FastMCP's stdio transport expects.

## 📚 Code Documentation

### Script Documentation (simulated_idp.py)
The `simulated_idp.py` script initializes a FastMCP server and defines an `extract` tool.
- The `extract` function takes `document` (string) and `entities` (list of strings) as input.
- It processes the document line by line, attempting to find and extract values for the specified entities using simple pattern matching (`entity: value` or `entity - value`).
- It returns a dictionary containing the extracted entities and messages for entities not found.
- The script runs the FastMCP server using `mcp.run(transport="stdio")`.

## 🔍 Architecture Feedback

Based on the `simulated_idp.py` script:

- **Overall Structure**:
  - **Strengths**: Simple, single-file implementation. Uses FastMCP to expose an `extract` tool. Clear separation of the extraction logic within the `extract` function.
  - **Areas for Improvement**: The current implementation is quite basic. Error handling within the `extract` function could be more robust (e.g., handling cases where the regex doesn't match after finding the entity name). The architecture feedback provided previously (Model, Controller, Presenter layers) might be overly complex for this current structure. A simpler approach to feedback focusing on the single script's design, the `extract` function's logic, and the use of FastMCP might be more appropriate.

## 🔄 Future Improvements

1. **Robust Extraction Logic**
   - Implement more sophisticated parsing methods (e.g., using actual parsing libraries instead of simple regex).
   - Improve error handling and edge case management within the extraction function.

2. **Input/Output Handling**
   - Provide clearer documentation or examples for interacting with the script via standard input/output using FastMCP's stdio transport.
   - Consider adding support for file input or other transport methods if needed.

3. **Feature Additions**
   - Support for batch processing.
   - Additional entity types and more flexible extraction rules.

## 🤝 Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request

## 📄 License

This project is open source and available under the MIT License.
