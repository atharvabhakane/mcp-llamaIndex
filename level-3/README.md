# Level 3 - MCP Entity Extraction System

## 🏁 Why I Built This

After connecting to real-world APIs, I wanted to see if I could extract useful information from documents themselves. This project is my hands-on journey into entity extraction: pulling out things like invoice numbers, dates, and totals from raw text. If you’re curious about how to automate document understanding, this is a great place to start!

---

## 🗂️ Project Structure

```
level-3/
├── simulated_idp.py  # FastMCP script for entity extraction
└── README.md         # This documentation
```

---

## 🚀 How to Run This (Step-by-Step)

1. **Install requirements:**
   ```bash
   pip install mcp
   ```
2. **Start the server:**
   ```bash
   python simulated_idp.py
   ```
3. **Test it!**
   - When the script is running, provide input as JSON:
     ```json
     {"document": "Invoice No: INV-12345 Customer: John Doe Date: 2024-06-01 Total: $100.00", "entities": ["invoice_number", "customer", "date", "total"]}
     ```
   - You'll get back:
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

## 🔄 How It Works (Flowchart)

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

---

## 🛠️ What Tool Is Included?

### `extract(document: str, entities: list[str]) -> dict`
Extracts specified entities from the provided document text.

- Input: `document` (string), `entities` (list of strings)
- Output: Dictionary with extracted values for each entity

---

## 💡 What You'll Learn
- How to process documents line by line
- How to extract key-value pairs using simple pattern matching
- Why input format and document structure matter

## 🧑‍💻 Why This Matters
This project taught me that real-world documents are messy! I ran into spacing and alignment issues, which led me to look for better solutions in the next level.

---

## 🖼️ Visual Example: Entity Extraction

### Input Example

![Entity Extraction Input](../Images/Screenshot%202025-07-09%20203433.png)
*This shows the input invoice and the entity extraction request, specifying the entities to extract (Invoice No, Date, Status).* 

### Output Example

![Entity Extraction Output](../Images/Screenshot%202025-07-09%20203424.png)
*This shows the extracted output for the requested entities: invoice number, date, and status.*

---

## ⚠️ Important Notes

- Run the `simulated_idp.py` script directly.
- The script interacts via standard input and standard output. The exact input format expected by FastMCP's stdio transport may require further investigation.
- The system works best with well-formatted text documents.
- Supported entities are determined by the logic within the `extract` function (currently includes basic patterns for entities followed by ':' or '-').

---

## 🙌 Ready to Learn or Contribute?

If you’ve made it this far—thank you! I built this project to help others learn, experiment, and build real solutions. Whether you’re a total beginner or an experienced developer, your questions and contributions are always welcome.

**Next Steps:**
- Try running the entity extraction tool and see what you can build.
- If you get stuck, open an issue or reach out—I'm happy to help!
- Want to add a new feature or fix a bug? Fork the repo and send a pull request.

Let’s make document processing easier, together!
