# from server_auth import _session_creds
from auth.middleware import _session_creds
from utils.context import get_session_id
from whatsapp.message_sending import WhatsAppClient
from mcp import McpError
from mcp.types import ErrorData


def get_whatsapp_client() -> WhatsAppClient:
    session_id = get_session_id()
    creds = _session_creds.get(session_id)

    if not creds:
        raise McpError(
            ErrorData(code=401, message="WhatsApp credentials missing")
        )

    return WhatsAppClient(
        phone_number_id=creds["phone_number_id"],
        access_token=creds["access_token"],
        api_version=creds["api_version"],
    )
