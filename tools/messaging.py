from typing import Dict, Any, Optional, List
from whatsapp.whatsapp_client import get_whatsapp_client
from mcp_setup import mcp

@mcp.tool
async def send_whatsapp_text_message(
    to: str,
    body: str,
    preview_url: bool = False,
) -> Dict[str, Any]:
    client = get_whatsapp_client()
    return await client.send_text(to, body, preview_url)


@mcp.tool
async def send_whatsapp_template_message(
    to: str,
    template_name: str,
    language_code: str = "en_US",
    components: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    client = get_whatsapp_client()
    return await client.send_template(
        to, template_name, language_code, components
    )
