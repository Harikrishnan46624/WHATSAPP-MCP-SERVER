from typing import Dict, Any
from mcp_setup import mcp
from whatsapp.whatsapp_client import get_whatsapp_client


@mcp.tool()
async def send_whatsapp_flow(
    to: str,
    flow_id: str,
    body_text: str,
    cta_text: str,
    flow_token: str,
    start_screen: str,
) -> Dict[str, Any]:
    """Send a WhatsApp flow message.

    Args:
        to (str): The recipient's phone number.
        flow_id (str): The ID of the flow.
        body_text (str): The body text of the message.
        cta_text (str): The call-to-action text.
        flow_token (str): The flow token.
        start_screen (str): The start screen.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    client = get_whatsapp_client()
    return await client.send_flow(
        to, flow_id, body_text, cta_text, flow_token, start_screen
    )
