from mcp_setup import mcp
from auth.middleware import WhatsAppAuthMiddleware

from tools.messaging import *
from tools.interactive import *
from tools.media import *
from tools.flows import *
import os


PORT = int(os.getenv("MCP_PORT", 2001))
TRANSPORT = os.getenv("MCP_TRANSPORT", "streamable-http")


mcp.add_middleware(WhatsAppAuthMiddleware())

if __name__ == "__main__":
    print(f"🚀 WhatsApp MCP Server running on port {PORT}")
    mcp.run(transport=TRANSPORT, port=PORT)
