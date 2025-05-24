# Project Feedback: LlamaParse MCP Server

This document provides feedback on the development and functionality of the LlamaParse MCP server.

## Tools Used

The following tools are implemented and exposed by the `server.py` file using the `fastmcp` framework:

-   `extract_entities`: This tool is designed to extract specific entities from a given PDF file path.
-   `test_connection`: A utility tool to verify the server's connectivity and check for the presence of the Llama Cloud API key.

## Potential Errors and Resolutions

During the development and operation of a system like this, several types of errors can potentially occur. Here are some common ones and their possible resolutions:

### 1. Missing API Key

-   **Error:** The `LLAMA_CLOUD_API_KEY` environment variable is not set or is empty.
-   **Resolution:** Ensure that a `.env` file is present in the project root with the correct API key: `LLAMA_CLOUD_API_KEY=your_api_key_here`. Alternatively, set the environment variable directly in your system or deployment environment.

### 2. File Not Found

-   **Error:** The specified `pdf_path` in the `extract_entities` tool request does not point to an existing file.
-   **Resolution:** Verify that the path provided in the request is correct and the PDF file exists at that location relative to where the server is running.

### 3. LlamaParse API Errors

-   **Error:** The call to the LlamaParse API fails due to various reasons such as invalid API key, rate limits, network issues, or problems with processing the document on the API side (e.g., malformed PDF).
-   **Resolution:** The server includes a fallback mechanism to process the text locally if the API call fails. For API-specific errors, check the API key, review the LlamaParse API documentation for error codes, ensure network connectivity, and verify the integrity of the PDF file.

### 4. PDF Processing Issues (Fallback)

-   **Error:** The fallback parsing mechanism fails to extract text from the PDF, or the extracted text is empty or garbled.
-   **Resolution:** This can happen with complex or image-based PDFs that are difficult to convert to text. The current simple entity extraction in the fallback relies on basic text patterns. For better results with challenging PDFs, consider integrating a more advanced local PDF parsing library or improving the pattern matching logic.

### 5. Encoding Problems

-   **Error:** Issues with character encoding lead to garbled text or errors when processing file contents or printing output, especially with non-ASCII characters.
-   **Resolution:** The `server.py` includes explicit encoding setup and utility functions (`ascii_safe_print`, `ultra_sanitize_text`) to mitigate these issues. Ensure the environment where the server runs is configured to support UTF-8, and continue using safe encoding practices when handling text data.

### 6. Entity Extraction Failures (Fallback)

-   **Error:** The `extract_simple_entities` function in the fallback might not find the requested entities even if they are present in the text, due to variations in formatting or phrasing.
-   **Resolution:** Improve the `extract_simple_entities` logic to use more flexible pattern matching (e.g., regular expressions) and handle different formats for the target entities (like dates or currency). Also, consider adding more specific extraction logic for different entity types.

### 7. Server Startup Failures

-   **Error:** The server fails to start.
-   **Resolution:** Check for dependency installation issues (`pip install -r requirements.txt`), errors in the `server.py` code, or conflicts with the port/transport being used by `fastmcp`. Review the console output for specific error messages during startup.

## Conclusion

Developing the MCP server involved implementing core functionality for PDF entity extraction with resilience through a fallback. Addressing potential errors related to API interaction, file handling, parsing, and encoding is crucial for building a robust system. Further improvements to error handling granularity and the fallback extraction logic can enhance the server's reliability and performance. 