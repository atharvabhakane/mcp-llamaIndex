# MCP Weather Service (Level 2)

A simple weather service that allows users to get current weather information for any location using the WeatherAPI.

## 🚀 Features

- Get current weather information for any location
- Simple command-line interface
- RESTful API endpoint
- Error handling and validation
- Environment variable support for API keys

## 📋 Prerequisites

- Python 3.7+
- FastAPI
- Requests
- python-dotenv
- WeatherAPI account and API key

## 🔧 Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install fastapi uvicorn requests python-dotenv
```
3. Create a `.env` file in the project root and add your WeatherAPI key:
```
WEATHER_API_KEY=your_api_key_here
```

## 🏗️ Project Structure

```
.
├── main.py          # FastAPI server implementation
├── client.py        # Command-line client
├── .env            # Environment variables (create this)
└── README.md       # This file
```

## 🔄 Flow

```mermaid
graph TD
    A[User] -->|Enters location| B[Client.py]
    B -->|POST request| C[FastAPI Server]
    C -->|API request| D[WeatherAPI]
    D -->|Weather data| C
    C -->|Formatted response| B
    B -->|Display result| A
```

## 🚀 Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. In a separate terminal, run the client:
```bash
python client.py
```

3. Enter a location when prompted

## 📡 API Endpoint

### POST /mcp

Request body:
```json
{
    "command": "weather",
    "location": "London"
}
```

Response:
```json
{
    "location": "London",
    "country": "United Kingdom",
    "temperature_c": 15.6,
    "condition": "Partly cloudy"
}
```

## ⚠️ Error Handling

The service handles various error cases:
- Missing location parameter
- Invalid API responses
- Network errors
- Invalid commands

## 🔒 Security

- API keys are stored in environment variables
- Input validation using Pydantic models
- Error messages don't expose sensitive information

## 🛠️ Development

To modify or extend the service:
1. The main server logic is in `main.py`
2. The client interface is in `client.py`
3. Add new commands by extending the `handle_mcp` function

## 📚 Code Documentation

The codebase follows comprehensive documentation practices:

### Server Documentation
- FastAPI route handlers are documented with detailed docstrings
- Request/Response models are documented using Pydantic
- API endpoints include OpenAPI/Swagger documentation
- Error handling and validation are clearly documented

### Client Documentation
- Command-line interface usage is documented
- Input validation and error handling are explained
- Example usage patterns are provided
- Configuration options are documented

### Code Comments
- Complex logic is explained with inline comments
- Function parameters and return values are documented
- Edge cases and error scenarios are noted
- API integration points are clearly marked

## 📊 MCP Feedback

### Architecture
- Clean separation of concerns between client and server
- RESTful API design following best practices
- Modular code structure for easy maintenance
- Scalable design for future extensions

### Performance
- Efficient API request handling
- Minimal response time for weather queries
- Optimized error handling
- Resource-efficient implementation

### Security
- Secure API key management
- Input validation and sanitization
- Error message security
- Environment variable protection

### User Experience
- Intuitive command-line interface
- Clear error messages
- Consistent response format
- Easy configuration

### Areas for Improvement
- Add caching for frequent requests
- Implement rate limiting
- Add more weather data points
- Support for historical weather data
- Add unit tests and integration tests

## 📝 License

This project is open source and available under the MIT License. 