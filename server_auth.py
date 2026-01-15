from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
from dotenv import load_dotenv
import os
from mcp import McpError
from mcp.types import ErrorData

load_dotenv()



# ---------------------------------------------------------------------
# ENV & GLOBAL STATE
# ---------------------------------------------------------------------

MCP_API_TOKEN = os.getenv("MCP_API_TOKEN")
if not MCP_API_TOKEN:
    raise RuntimeError("❌ MCP_API_TOKEN not found in .env")


_session_creds: dict[str, dict[str, str]] = {}



# ---------------------------------------------------------------------
# AUTH MIDDLEWARE
# ---------------------------------------------------------------------

class WhatsAppAuthMiddleware(Middleware):
    """
    Validates MCP token and extracts WhatsApp credentials
    into session-scoped memory.
    """

    async def on_request(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()

        # ---- MCP AUTH ----
        if headers.get("authorization") != f"Bearer {MCP_API_TOKEN}":
            raise McpError(ErrorData(code=401, message="Unauthorized MCP token"))

        # ---- WhatsApp credentials ----
        phone_number_id = headers.get("x-whatsapp-phone-id", "").strip()
        access_token = headers.get("x-whatsapp-token", "").strip()
        api_version = headers.get("x-whatsapp-api-version", "v18.0").strip() or "v18.0"

        if not phone_number_id or not access_token:
            raise McpError(
                ErrorData(code=401, message="Missing WhatsApp credentials headers")
            )

        try:
            session_id = context.fastmcp_context.session_id or "default"
        except Exception:
            session_id = "default"

        _session_creds[session_id] = {
            "phone_number_id": phone_number_id,
            "access_token": access_token,
            "api_version": api_version,
        }

        return await call_next(context)