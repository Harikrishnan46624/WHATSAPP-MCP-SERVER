from typing import Dict, Any, List
from whatsapp.whatsapp_client import get_whatsapp_client
from mcp_setup import mcp

@mcp.tool()
async def send_whatsapp_list(
    to: str,
    header_text: str,
    body_text: str,
    footer_text: str,
    button_text: str,
    sections: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Send a WhatsApp interactive list message.

    Args:
        to (str): The recipient's phone number.
        header_text (str): The header text.
        body_text (str): The body text.
        footer_text (str): The footer text.
        button_text (str): The button text.
        sections (List[Dict[str, Any]]): The sections for the list.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    client = get_whatsapp_client()
    return await client.send_interactive_list(
        to, header_text, body_text, footer_text, button_text, sections
    )


@mcp.tool()
async def send_whatsapp_confirmation_buttons(
    to: str,
    message: str,
    footer_text: str = "Please confirm",
) -> Dict[str, Any]:
    """Send a WhatsApp message with confirmation buttons.

    Args:
        to (str): The recipient's phone number.
        message (str): The message text.
        footer_text (str, optional): The footer text. Defaults to "Please confirm".

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    buttons = [
        {"type": "reply", "reply": {"id": "confirm", "title": "Confirm"}},
        {"type": "reply", "reply": {"id": "edit", "title": "Edit"}},
    ]

    client = get_whatsapp_client()
    return await client.send_interactive_buttons(
        to, message, footer_text, buttons
    )
