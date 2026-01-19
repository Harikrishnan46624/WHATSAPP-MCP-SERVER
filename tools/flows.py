from typing import Dict, Any
from mcp_setup import mcp
from whatsapp.whatsapp_client import get_whatsapp_client


@mcp.tool
async def send_whatsapp_flow(
    to: str,
    flow_id: str,
    body_text: str,
    cta_text: str,
    flow_token: str,
    start_screen: str,
) -> Dict[str, Any]:
    client = get_whatsapp_client()
    return await client.send_flow(
        to, flow_id, body_text, cta_text, flow_token, start_screen
    )
