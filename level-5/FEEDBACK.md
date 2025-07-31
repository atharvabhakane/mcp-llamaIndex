# Project Feedback: MCP LlamaExtract Dynamic Server

This feedback is a straight-up summary of how the dynamic schema-based LlamaExtract MCP server turned out, what issues we ran into, and how they got fixed. The whole idea was to make extraction flexible — no predefined fields, just let the user decide what to pull from a document.

---

## What This Server Does

The FastMCP server is built around the LlamaExtract SDK and has a single, powerful tool:

### ✅ `extract_entities_dynamic`

* Accepts a list of entities (as strings) and a document (via `pdf_path` or `pdf_base64`)
* Dynamically creates a Pydantic schema using `create_model()` for those entities
* Either fetches or creates a new agent in LlamaExtract based on the input entities
* Extracts data from the document using that agent and sends it back as JSON

This avoids hardcoding any schema and gives full control to the end user.

---

## Errors We Faced (and Fixed)

### 🔸 `ImportError` from `llama_cloud_services`

* **Problem:** Trying to import `SourceText`, which isn’t part of the SDK anymore (we’re using v0.6.41).
* **Fix:** Removed `SourceText` usage and simplified file input to use direct paths or base64 decoding.

---

### 🔸 Agent creation failed silently

* **Problem:** Sometimes agents weren’t getting created at all.
* **Cause:** Invalid or malformed dynamic schema or missing error handling around `create_agent()`.
* **Fix:** Added better exception handling and schema validation before calling the LlamaExtract SDK.

---

### 🔸 MCP Timeout (`error -32001`)

* **Problem:** The MCP server timed out waiting for LlamaExtract agent creation or extraction.
* **Fixes:**

  * Reduced unnecessary operations in the extract function
  * Moved to use `pdf_path` (Claude can’t send base64 easily)
  * Ensured we only create agents if they don’t already exist
  * Avoided extra MCP tool functions that could slow things down

---

### 🔸 Claude couldn’t send files

* **Problem:** Claude doesn’t send PDFs as base64, but our first version only accepted `pdf_base64`.
* **Fix:** Updated the server to accept both `pdf_path` and `pdf_base64` (with file existence check), so Claude works seamlessly.

---

## What Worked Well

* The **factory pattern** using `create_model()` for dynamic schema worked exactly as planned.
* Caching agents based on entity names prevented repeated re-creation.
* FastMCP setup stayed consistent with earlier levels, making it easy to plug this in.

---

## What Could Be Better

* We could clean up the `agent_name` logic and maybe hash the entity list instead of joining strings
* Right now all fields are treated as strings — handling arrays, dates, or optional fields would make this more robust
* Errors returned from the SDK could be surfaced in a more readable format (instead of raw exceptions)

---

## Final Notes

This server now gives you the ability to extract exactly what you need from any document, on demand, without touching the code for each new field. It’s flexible, clean, and working as expected with Claude + FastMCP. You’re good to go for Level 5.

Let me know if you want to add screenshots, schema examples, or test results to this. 