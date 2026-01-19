from typing import Dict, Any, Optional
from whatsapp.whatsapp_client import get_whatsapp_client
from utils.validation import require_exactly_one
from mcp_setup import mcp

@mcp.tool
async def send_whatsapp_document(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    filename: Optional[str] = None,
    caption: Optional[str] = None,
) -> Dict[str, Any]:
    require_exactly_one(media_id=media_id, link=link)
    client = get_whatsapp_client()
    return await client.send_document(
        to, media_id, link, filename, caption
    )


@mcp.tool
async def send_whatsapp_image(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    caption: Optional[str] = None,
) -> Dict[str, Any]:
    require_exactly_one(media_id=media_id, link=link)
    client = get_whatsapp_client()
    return await client.send_image(to, media_id, link, caption)
