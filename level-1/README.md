# Level 1 - MCP Calculator Server

## ✨ Why I Started Here

When I first began exploring the Model Context Protocol (MCP), I wanted to start with something simple and approachable—a calculator! This project is my way of learning (and teaching) the basics of MCP, FastMCP, and async Python, all in one place. If you're new to MCP or just want to see how the pieces fit together, this is the perfect starting point.

---

## 📆 Project Structure

```text
level-1/
├── server.py          # MCP Server exposing tools
├── mcp.json           # Configuration to connect via Cursor or MCP Inspector
└── README.md          # Documentation
```

---

## 🔄 How It Works (Flowchart)

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

## 🛠️ What Tools Are Included?

### 1. `add`
Adds two numbers together.

```python
@mcp.tool()
async def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b
```

### 2. `subtract`
Subtracts the second number from the first.

```python
@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Subtract second number from the first."""
    return a - b
```

### 3. `hello`
Greets you by name.

```python
@mcp.tool()
async def hello(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}! Welcome to the MCP calculator!"
```

---

## 🚀 How to Run This (Step-by-Step)

1. **Install FastMCP:**
   ```bash
   pip install fastmcp
   ```
2. **Start the server:**
   ```bash
   python server.py
   ```
3. **Test it!**
   - Using MCP Inspector:
     - Run:
       ```bash
       npx @modelcontextprotocol/inspector
       ```
     - Paste the path to your `server.py` and select transport: `stdio`.
     - Use a test payload like:
       ```json
       { "tool": "add", "args": { "a": 5, "b": 3 } }
       ```
     - You’ll get back:
       ```json
       { "result": 8 }
       ```
   - Using Cursor/Claude:
     - Upload your config:
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
     - Then type in chat: `Add 5 and 10`

---

## 💡 What You'll Learn
- How to define and expose tools using FastMCP
- How to run and test an MCP server
- How requests flow from user to tool and back

## 🧑‍💻 Why This Matters
Getting this running gave me a solid foundation for everything that comes next. If you can get this working, you’re ready for more advanced tools!

---

## 🖼️ Visual Example: Using the MCP Calculator Tool

![MCP Calculator Example](../Images/Screenshot%202025-07-09%20201953.png)
*This shows the use of the MCP calculator tool to compute 3+4, including the request sent to the tool and the response received (3 + 4 = 7).* 

#### Subtract Tool Example

![MCP Subtract Example](../Images/Screenshot%202025-07-09%20202324.png)
*This shows the use of the MCP subtract tool to compute 10-7, including the request and the response (10 - 7 = 3).* 

#### Hello Tool Example

![MCP Hello Example](../Images/Screenshot%202025-07-09%20202419.png)
*This shows the use of the MCP hello tool, which returns a greeting message in response to the input.*

---

## 🙌 Ready to Learn or Contribute?

If you’ve made it this far—thank you! I built this project to help others learn, experiment, and build real solutions. Whether you’re a total beginner or an experienced developer, your questions and contributions are always welcome.

**Next Steps:**
- Try running the calculator and see what you can build.
- If you get stuck, open an issue or reach out—I'm happy to help!
- Want to add a new feature or fix a bug? Fork the repo and send a pull request.

Let’s make document processing easier, together!
