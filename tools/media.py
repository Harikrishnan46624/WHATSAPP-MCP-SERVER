from typing import Dict, Any, Optional
from whatsapp.whatsapp_client import get_whatsapp_client
from utils.validation import require_exactly_one
from mcp_setup import mcp

@mcp.tool()
async def send_whatsapp_document(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    filename: Optional[str] = None,
    caption: Optional[str] = None,
) -> Dict[str, Any]:
    """Send a WhatsApp document message.

    Args:
        to (str): Recipient's phone number in international format **without** the '+' prefix,
          starting with the country code (e.g., "919876543210").
        media_id (Optional[str]): The media ID. Either media_id or link must be provided.
        link (Optional[str]): The link to the document. Either media_id or link must be provided.
        filename (Optional[str]): The filename.
        caption (Optional[str]): The caption.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    require_exactly_one(media_id=media_id, link=link)
    client = get_whatsapp_client()
    return await client.send_document(
        to, media_id, link, filename, caption
    )


@mcp.tool()
async def send_whatsapp_image(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    caption: Optional[str] = None,
) -> Dict[str, Any]:
    """Send a WhatsApp image message.

    Args:
        to (str): Recipient's phone number in international format **without** the '+' prefix,
        starting with the country code (e.g., "919876543210").
        media_id (Optional[str]): The media ID. Either media_id or link must be provided.
        link (Optional[str]): The link to the image. Either media_id or link must be provided.
        caption (Optional[str]): The caption.

    Returns:
        Dict[str, Any]: The response from the WhatsApp API.
    """
    require_exactly_one(media_id=media_id, link=link)
    client = get_whatsapp_client()
    return await client.send_image(to, media_id, link, caption)
