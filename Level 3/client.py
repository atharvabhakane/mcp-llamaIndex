import requests
import json

def main():
    print("📄 MCP Client – Simulated IDP (Level 3)")
    
    # Define supported entities
    SUPPORTED_ENTITIES = {
        "invoice_number": "Invoice Number",
        "customer": "Customer Name",
        "date": "Date",
        "total": "Total Amount"
    }
    
    print("Supported entities:")
    for entity, description in SUPPORTED_ENTITIES.items():
        print(f"- {entity}: {description}")
    print()

    # Take document input from user
    document = input("Enter document text (single line):\n> ").strip()

    # Take entity list input
    entity_input = input("\nEnter entities to extract (comma-separated):\n> ")
    entities = [e.strip().lower() for e in entity_input.split(",") if e.strip()]

    # Validate entities
    invalid_entities = [e for e in entities if e not in SUPPORTED_ENTITIES]
    if invalid_entities:
        print("\n❌ Error: Invalid entity names detected:")
        for entity in invalid_entities:
            print(f"- '{entity}' is not a valid entity name")
        print("\nPlease use only these entity names:")
        for entity in SUPPORTED_ENTITIES:
            print(f"- {entity}")
        return

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

        print("\n🧠 Extracted Entities:")
        print(json.dumps(result, indent=2))

    except requests.exceptions.RequestException as e:
        print("\n❌ Error: Failed to connect to MCP server")
        print("Make sure the server is running at http://localhost:8000")
        print(f"Technical details: {e}")

if __name__ == "__main__":
    main()
