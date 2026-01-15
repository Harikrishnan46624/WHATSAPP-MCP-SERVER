# WhatsApp MCP Server

A Model Context Protocol (MCP) server that connects to the WhatsApp Cloud API, enabling Large Language Models (LLMs) to send messages, templates, and interactive menus via WhatsApp.

## Features

- **Send Text Messages**: Send free-form text messages.
- **Send Template Messages**: Send approved WhatsApp templates (utility, marketing, authentication).
- **Send Interactive Lists**: Send selection menus to users.
- **Secure Authentication**: Uses per-request credential injection via headers.

## Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- WhatsApp Cloud API Credentials:
  - Phone Number ID
  - Permanent/System User Access Token

## Configuration

1. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```bash
   MCP_API_TOKEN=your_secure_random_token_here
   ```

2. **Client Headers**:
   When connecting to this MCP server, your client must provide the following headers:
   - `Authorization`: `Bearer <MCP_API_TOKEN>`
   - `x-whatsapp-phone-id`: Your WhatsApp Phone Number ID
   - `x-whatsapp-token`: Your WhatsApp Cloud API Access Token
   - `x-whatsapp-api-version`: (Optional) API version, e.g., `v18.0`

## Local Development

To run the server locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python whatsapp_mcp_server.py
   ```
   The server will start on port `2001`.

## Docker Deployment

### Build and Run

When you edit code, rebuild and run the container:

```bash
# Build the image
docker build -t whatsapp-mcp:latest .

# Run the container
docker run --rm -p 2001:2001 whatsapp-mcp:latest
```

### Clean Build

If you suspect cache issues or want a completely clean build:

```bash
docker build --no-cache --pull -t whatsapp-mcp:latest .
docker run --rm -p 2001:2001 whatsapp-mcp:latest
```

## Tools

The server exposes the following MCP tools:

- `send_whatsapp_text_message(to, body, preview_url)`
- `send_whatsapp_template_message(to, template_name, language_code, components)`
- `send_whatsapp_service_options_menu(to, header_text, body_text, footer_text, button_text, sections)`
