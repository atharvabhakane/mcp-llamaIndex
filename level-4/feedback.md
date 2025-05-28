# Project Feedback: LlamaParse MCP Server

This document provides feedback on the development and functionality of the LlamaParse MCP server.

## Tools Used

The following tools are implemented and exposed by the `server.py` file using the `fastmcp` framework:

-   `extract_entities`: This tool is designed to extract specific entities from a given PDF file path or base64 encoded string using the LlamaParse API.
-   `test_connection`: A utility tool to verify the server's connectivity and check for the presence of the Llama Cloud API key.

## Potential Errors and Resolutions

During the development and operation of a system like this, several types of errors can potentially occur. Here are some common ones and their possible resolutions:

### 1. Missing API Key

-   **Error:** The `LLAMA_CLOUD_API_KEY` environment variable is not set or is empty.
-   **Resolution:** Ensure that a `.env` file is present in the project root with the correct API key: `LLAMA_CLOUD_API_KEY=your_api_key_here`. Alternatively, set the environment variable directly in your system or deployment environment.

### 2. File Not Found (if using pdf_path)

-   **Error:** The specified `pdf_path` in the `extract_entities` tool request does not point to an existing file.
-   **Resolution:** Verify that the path provided in the request is correct and the PDF file exists at that location relative to where the server is running.

### 3. LlamaParse API Errors

-   **Error:** The call to the LlamaParse API fails due to various reasons such as invalid API key, rate limits, network issues, or problems with processing the document on the API side (e.g., malformed PDF).
-   **Resolution:** Check the API key, review the LlamaParse API documentation for error codes, ensure network connectivity, and verify the integrity of the PDF file.

### 4. Encoding Problems

-   **Error:** Issues with character encoding lead to garbled text or errors when processing file contents or printing output, especially with non-ASCII characters.
-   **Resolution:** The `server.py` includes explicit encoding setup to mitigate these issues. Ensure the environment where the server runs is configured to support UTF-8, and continue using safe encoding practices when handling text data.

### 5. Server Startup Failures

-   **Error:** The server fails to start.
-   **Resolution:** Check for dependency installation issues (`pip install -r requirements.txt`), errors in the `server.py` code, or conflicts with the port/transport being used by `fastmcp`. Review the console output for specific error messages during startup.

## Conclusion

Developing the MCP server involved implementing core functionality for PDF entity extraction using the LlamaParse API. Addressing potential errors related to API interaction, file handling, and encoding is crucial for building a robust system. Further improvements to error handling granularity can enhance the server's reliability and performance. 