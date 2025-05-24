# Level 1 - MCP Calculator Server

## ✨ Project Overview

This is a basic **Model Context Protocol (MCP)** server built using **FastMCP** in Python. It exposes simple arithmetic tools (`add`, `subtract`, and `hello`) as callable functions through a standard MCP interface.

This is intended as **Level 1** of the MCP IDP project, demonstrating a minimal end-to-end MCP server setup that can integrate with AI tools like **Claude**, **Cursor**, or **MCP Inspector**.

---

## 📆 Project Structure

```text
level-1/
├── server.py          # MCP Server exposing tools
├── mcp.json           # Configuration to connect via Cursor or MCP Inspector
└── README.md          # Documentation
```

---

## 🔄 Flowchart

```text
+------------------+       +-------------------------+
| User (in chat)   |  -->  | Claude/Cursor/Inspector |
+------------------+       +-------------------------+
                                   |
                                   v
                        +---------------------+
                        | MCP Server (FastMCP)|
                        | Tools: add, subtract|
                        +---------------------+
                                   |
                                   v
                         +--------------------+
                         | Returns result JSON|
                         +--------------------+
```

---

## 🔧 Tools Implemented

### 1. `add`

```python
@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
```

### 2. `subtract`

```python
@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Subtract second number from the first."""
    return a - b
```

### 3. `hello`

```python
@mcp.tool()
async def hello(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}! Welcome to the MCP calculator!"
```

---

## 📖 How to Run the Server

### Step 1: Install Requirements

```bash
pip install fastmcp
```

### Step 2: Run the Server

```bash
python server.py
```

---

## 🔍 How to Test

### Using MCP Inspector:

* Run MCP Inspector with:

```bash
npx @modelcontextprotocol/inspector
```

* Paste the path to your `server.py`
* Select transport: `stdio`
* Use test payloads like:

```json
{
  "tool": "add",
  "args": { "a": 5, "b": 3 }
}
```

### Using Cursor/Claude:

* Upload your config:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["C:/path/to/level-1/server.py"]
    }
  }
}
```

* Then type in chat:

> "Add 5 and 10"

---

## 📅 Sample MCP Responses

```json
{
  "result": 15
}
```

```json
{
  "response": "Hello, Alice! Welcome to the MCP calculator!"
}
```

---

## 📄 Code With Documentation

Each function is:

* Annotated with docstrings
* Uses proper type hints
* Fully exposed as a tool using `@mcp.tool()`

The server uses `mcp.run(transport="stdio")` for MCP integration.

---

## 🔍 Feedback on Level 1 Project

### Pros:

* Easy to understand
* Tools are simple and testable
* Useful starter for understanding MCP integration

### Improvement Suggestions:

* Support multiple input values (e.g. `add(1,2,3,4)`)  
* Add error handling and input validation
* Add unit tests

---

## 💡 Tip

Want to simulate this with Claude or Cursor? Use prompts like:

> "What is the result of subtracting 7 from 20?"

It will call your MCP tool under the hood!

---

## 📁 License

MIT License

---

Happy Coding! 🚀
