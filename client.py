import requests
import json

def main():
    print("📄 MCP Client – Simulated IDP (Level 3)")
    print("Supported entities: invoice_number, customer, date, total\n")

    # Take document input from user
    document = input("Enter document text (single line):\n> ").strip()

    # Take entity list input
    entity_input = input("\nEnter entities to extract (comma-separated):\n> ")
    entities = [e.strip() for e in entity_input.split(",") if e.strip()]

    # Build payload
    payload = {
        "command": "extract",
        "document": document,
        "entities": entities
    }

    try:
        # Send request to MCP server
        response = requests.post("http://localhost:8000/mcp", json=payload)
        result = response.json()

        print("\n🧠 Extracted Entities (Simulated):")
        print(json.dumps(result, indent=2))

    except requests.exceptions.RequestException as e:
        print("❌ Failed to connect to MCP server:", e)

if __name__ == "__main__":
    main()
