from typing import Dict, Any, Optional, List
from whatsapp.whatsapp_client import get_whatsapp_client
from mcp_setup import mcp

@mcp.tool()
async def send_whatsapp_text_message(
    to: str,
    body: str,
    preview_url: bool = False,
) -> Dict[str, Any]:
    """Send a WhatsApp text message.

    Args:
        to (str): Recipient's phone number in international format **without** the '+' prefix,
        starting with the country code (e.g., "919876543210").
        body (str): The message body.
        preview_url (bool, optional): Whether to preview URLs. Defaults to False.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    client = get_whatsapp_client()
    return await client.send_text(to, body, preview_url)



@mcp.tool()
async def send_whatsapp_template_message(
    to: str,
    template_name: str,
    language_code: str,
    components: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Send a WhatsApp template message.

    Args:
       to (str): Recipient's phone number in international format **without** the '+' prefix,
        starting with the country code (e.g., "919876543210").
        template_name (str): The name of the template.
        language_code (str): The language code (MANDATORY, e.g. 'en_US').
        components (Optional[List[Dict[str, Any]]]): The template components.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    client = get_whatsapp_client()

    return await client.send_template(
        to=to,
        template_name=template_name,
        language_code=language_code,
        components=components,
    )
