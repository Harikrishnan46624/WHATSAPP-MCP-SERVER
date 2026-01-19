# WhatsApp MCP Server

A production-grade Model Context Protocol (MCP) server for the WhatsApp Cloud API, built with FastMCP. Designed for agent-first workflows, scalability, and clean operational practices.

## ✨ Features

* **Session-aware WhatsApp clients** with per-session credential management
* **Comprehensive messaging support**: text, template, media, and interactive messages
* **WhatsApp Flows integration** for advanced conversational experiences
* **Agent-friendly MCP tools** with structured inputs and outputs
* **Multi-tenant safe** with proper authentication and session isolation
* **Modern Python packaging** with pyproject.toml and uv support

## 🚀 Quick Start

### Prerequisites

* Python >= 3.14
* WhatsApp Cloud API credentials (Phone Number ID, Access Token)
* MCP API Token for authentication

### Local Development

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd whatsapp-mcp-server
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MCP_API_TOKEN
   ```

3. **Run the server:**
   ```bash
   python server.py
   ```

The server will start on port 2001 by default.

### Docker Deployment

#### Build the Image

```bash
docker build -t whatsapp-mcp-server .
```

#### Run Locally

```bash
docker run -p 2001:2001 whatsapp-mcp-server
```

#### Run with Environment Variables

```bash
docker run -p 2001:2001 \
  -e MCP_API_TOKEN=your_token_here \
  -e MCP_PORT=2001 \
  --name whatsapp-mcp-server whatsapp-mcp-server
```

#### Development with Hot Reload

```bash
docker run -p 2001:2001 \
  -v $(pwd):/app \
  whatsapp-mcp-server uvicorn app:app --host 0.0.0.0 --port 2001 --reload
```

## 🛠️ Available Tools

The MCP server provides the following WhatsApp tools:

### Messaging Tools
- `send_whatsapp_text_message` - Send text messages with URL preview support
- `send_whatsapp_template_message` - Send WhatsApp template messages

### Media Tools
- `send_whatsapp_document` - Send document files
- `send_whatsapp_image` - Send images with captions

### Interactive Tools
- `send_whatsapp_list` - Send interactive list messages
- `send_whatsapp_confirmation_buttons` - Send messages with confirmation buttons

### Flow Tools
- `send_whatsapp_flow` - Send WhatsApp Flow messages

## 🔐 Authentication

The server uses dual authentication:

1. **MCP API Token**: Bearer token authentication
   ```
   Authorization: Bearer <MCP_API_TOKEN>
   ```

2. **WhatsApp Credentials**: Per-request headers
   ```
   X-WhatsApp-Phone-ID: <phone_number_id>
   X-WhatsApp-Token: <access_token>
   X-WhatsApp-API-Version: v18.0  # Optional, defaults to v18.0
   ```

## 📋 API Endpoints

- **MCP Endpoint**: `http://localhost:2001/mcp`

### Testing the MCP Endpoint

```bash
# List available tools
curl -X POST http://localhost:2001/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_mcp_token" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'

# Send a text message
curl -X POST http://localhost:2001/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_mcp_token" \
  -H "X-WhatsApp-Phone-ID: your_phone_id" \
  -H "X-WhatsApp-Token: your_access_token" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 2,
    "params": {
      "name": "send_whatsapp_text_message",
      "arguments": {
        "to": "1234567890",
        "body": "Hello from MCP!"
      }
    }
  }'
```

## ⚙️ Environment Variables

| Variable       | Description              | Required | Default |
| -------------- | ------------------------ | -------- | ------- |
| `MCP_API_TOKEN` | MCP server authentication token | Yes | - |
| `MCP_PORT`     | Server port              | No      | 2001   |
| `MCP_TRANSPORT`| Transport protocol       | No      | streamable-http |

## 🏭 Production Deployment

### Docker Compose Example

```yaml
version: '3.8'
services:
  whatsapp-mcp:
    build: .
    ports:
      - "2001:2001"
    environment:
      - MCP_API_TOKEN=your_secure_token
      - MCP_PORT=2001
    restart: unless-stopped
```

### Using with MCP Clients

This server is designed to work with MCP-compatible clients such as:
- Claude Desktop
- Custom AI agents
- MCP client libraries

### Monitoring

```bash
# View container logs
docker logs whatsapp-mcp-server
```

## 📁 Project Structure

```
whatsapp-mcp-server/
├── app.py                 # HTTP app entry point
├── server.py              # MCP server setup and tools
├── mcp_setup.py           # FastMCP initialization
├── pyproject.toml         # Project configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── auth/                  # Authentication middleware
├── tools/                 # MCP tool implementations
├── whatsapp/              # WhatsApp client logic
└── utils/                 # Utility functions
```

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -e .

# Run tests (if available)
pytest
```

### Code Style

The project follows standard Python formatting. Consider using:
- Black for code formatting
- isort for import sorting
- flake8 for linting

## 📌 Use Cases

* **Agentic AI systems** using MCP for WhatsApp integration
* **Automated customer support** with conversational flows
* **Notification services** with rich media support
* **Multi-tenant messaging platforms**
* **LLM-powered chatbots** with WhatsApp connectivity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**Built for reliability, extensibility, and agent-first architectures with the WhatsApp Cloud API.**
