# import os
# import httpx
# from typing import Any

# from fastmcp import FastMCP
# from fastmcp.server.middleware import Middleware, MiddlewareContext
# from fastmcp.server.dependencies import get_http_headers
# from mcp import McpError
# from mcp.types import ErrorData
# from dotenv import load_dotenv

# # Load .env FIRST (MCP_API_TOKEN must be in .env)
# load_dotenv()

# # GLOBAL STATE: Store creds per session
# _session_creds: dict[str, dict[str, str]] = {}


# class WhatsAppAuthMiddleware(Middleware):
#     async def on_request(self, context: MiddlewareContext, call_next):
#         headers = get_http_headers()
#         print(f"DEBUG: Received headers: {dict(headers)}")

#         # 1. Validate MCP_API_TOKEN FROM .env ONLY
#         mcp_api_token = os.getenv("MCP_API_TOKEN")
#         if not mcp_api_token:
#             raise McpError(
#                 ErrorData(code=500, message="MCP_API_TOKEN not found in .env")
#             )

#         mcp_auth = headers.get("authorization", "")
#         expected_mcp = f"Bearer {mcp_api_token}"
#         if mcp_auth != expected_mcp:
#             raise McpError(
#                 ErrorData(code=401, message="Unauthorized MCP token")
#             )

#         # 2. Extract WhatsApp credentials from the headers your client actually sends
#         phone_number_id = headers.get("x-whatsapp-phone-id", "").strip()
#         access_token = headers.get("x-whatsapp-token", "").strip()
#         api_version = headers.get("x-whatsapp-api-version", "v18.0").strip() or "v18.0"

#         if not phone_number_id:
#             raise McpError(
#                 ErrorData(code=401, message="Missing x-whatsapp-phone-id header")
#             )
#         if not access_token:
#             raise McpError(
#                 ErrorData(code=401, message="Missing x-whatsapp-token header")
#             )

#         # 3. Store in session-scoped state
#         try:
#             # Prefer FastMCP session id if available
#             if context.fastmcp_context and context.fastmcp_context.request_context:
#                 session_id = context.fastmcp_context.session_id or "default"
#             else:
#                 # Fallback to header or default
#                 session_id = headers.get("mcp-session-id") or "default"
#         except Exception:
#             session_id = "default"

#         _session_creds[session_id] = {
#             "whatsapp_phone_number_id": phone_number_id,
#             "whatsapp_access_token": access_token,
#             "whatsapp_api_version": api_version,
#         }

#         print(
#             f"✅ Stored creds for session {session_id}: "
#             f"PNID={phone_number_id[:8]}..., api_version={api_version}"
#         )

#         return await call_next(context)


# # Create MCP server
# mcp = FastMCP("whatsapp-mcp-server")

# # Validate MCP_API_TOKEN from .env
# mcp_api_token = os.getenv("MCP_API_TOKEN")
# if not mcp_api_token:
#     raise RuntimeError("❌ MCP_API_TOKEN not found in .env file!")

# print(f"✅ MCP_API_TOKEN loaded from .env: {mcp_api_token[:10]}...")

# mcp.add_middleware(WhatsAppAuthMiddleware())

# @mcp.tool
# async def send_whatsapp_text(
#     to: str,
#     body: str,
#     preview_url: bool = False  # ← FIXED: Added missing parameter
# ) -> dict[str, Any]:
#     """
#     Send a WhatsApp text message using WhatsApp Cloud API (production-tested pattern).
    
#     Args:
#         to: Recipient phone number (e.g., "919876543210")
#         body: Message text content
#         preview_url: Enable link preview (default: False)
#     """
#     print(f"📞 Calling send_whatsapp_text(to={to}, body={body[:50]}...)")
    
#     # Get session credentials
#     try:
#         ctx = MiddlewareContext.current()
#         session_id = getattr(ctx, 'session_id', 'default') or 'default'
#     except:
#         session_id = 'default'
    
#     wa_creds = _session_creds.get(session_id)
#     if not wa_creds:
#         raise McpError(
#             ErrorData(code=500, message=f"WhatsApp credentials not available for session {session_id}")
#         )
    
#     phone_number_id = wa_creds["whatsapp_phone_number_id"]
#     access_token = wa_creds["whatsapp_access_token"]
#     api_version = wa_creds["whatsapp_api_version"]

#     print(f"PHONE NUMBER ID: {phone_number_id}")
#     print(f"ACCESS TOKEN: {access_token[:10]}...")
#     print(f"API VERSION: {api_version}")
    
#     # YOUR EXACT URL PATTERN
#     URL = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
    
#     # YOUR EXACT PAYLOAD (production-tested)
#     payload = {
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": to,
#         "type": "text",
#         "text": {
#             "preview_url": preview_url,  # ← FIXED: Now uses parameter
#             "body": body
#         }
#     }
    
#     # YOUR EXACT HEADERS
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
    
#     print(f"📱 Sending WhatsApp to {to}: {body[:50]}...")
    
#     async with httpx.AsyncClient(timeout=15.0) as client:
#         try:
#             resp = await client.post(URL, headers=headers, json=payload)
            
#             if resp.status_code == 200:
#                 result = resp.json()
#                 print(f"✅ Message sent successfully to {to} - Status Code: {resp.status_code}")
#                 print(f"📨 Message ID: {result.get('messages', [{}])[0].get('id', 'N/A')}")
#                 return result
            
#             # YOUR EXACT ERROR HANDLING
#             error_details = resp.json().get('error', {})
#             error_msg = error_details.get('message', 'Unknown error')
            
#             print(f"❌ Error sending message to {to}: {error_msg}")
            
#             raise McpError(
#                 ErrorData(
#                     code=resp.status_code,
#                     message=f"WhatsApp API failed: {error_msg}"
#                 )
#             )
            
#         except httpx.HTTPStatusError as e:
#             print(f"❌ HTTP error {e.response.status_code}: {e}")
#             raise McpError(
#                 ErrorData(code=e.response.status_code, message="WhatsApp API HTTP error")
#             )
#         except Exception as e:
#             print(f"❌ Unexpected error: {e}")
#             return {"error": str(e)}

# if __name__ == "__main__":
#     print("🚀 WhatsApp MCP Server starting on port 2001 (MCP_API_TOKEN from .env)...")
#     mcp.run(transport="streamable-http", port=2001)







from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
from fastmcp.server.middleware import MiddlewareContext
from mcp import McpError
from mcp.types import ErrorData
from server_auth import _session_creds, WhatsAppAuthMiddleware
from whatsapp_msg_sender import WhatsAppClient

# ---------------------------------------------------------------------
# SESSION → CLIENT RESOLVER
# ---------------------------------------------------------------------


def get_whatsapp_client() -> WhatsAppClient:
    try:
        ctx = MiddlewareContext.current()
        session_id = getattr(ctx, "session_id", "default") or "default"
    except Exception:
        session_id = "default"

    creds = _session_creds.get(session_id)
    if not creds:
        raise McpError(
            ErrorData(code=500, message="WhatsApp credentials not available")
        )

    return WhatsAppClient(
        phone_number_id=creds["phone_number_id"],
        access_token=creds["access_token"],
        api_version=creds["api_version"],
    )


# ---------------------------------------------------------------------
# MCP SERVER & TOOLS
# ---------------------------------------------------------------------

mcp = FastMCP("whatsapp-mcp-server")
mcp.add_middleware(WhatsAppAuthMiddleware())



@mcp.tool
async def send_whatsapp_text_message(
    to: str,
    body: str,
    preview_url: bool = False,
) -> dict[str, Any]:
    """
    Send a plain text WhatsApp message to a single recipient.

    This tool uses the WhatsApp Cloud API to deliver a free-form text message.
    It should be used for:
    - Notifications
    - Alerts
    - Ad-hoc messages
    - Non-templated communication

    Args:
        to (str):
            Recipient WhatsApp number in international format.
            Example: "919876543210"

        body (str):
            The text message content to send.

        preview_url (bool, optional):
            Whether WhatsApp should generate a rich preview for URLs
            present in the message body.
            Defaults to False.

    Returns:
        dict[str, Any]:
            Raw WhatsApp Cloud API response containing message ID
            and delivery metadata.

    Raises:
        McpError:
            If WhatsApp credentials are missing or the API request fails.
    """
    client = get_whatsapp_client()
    return await client.send_text(
        to=to,
        body=body,
        preview_url=preview_url,
    )


@mcp.tool
async def send_whatsapp_template_message(
    to: str,
    template_name: str,
    language_code: str = "en_US",
    components: Optional[List[Dict[str, Any]]] = None,
) -> dict[str, Any]:
    """
    Send a WhatsApp template message with fully dynamic components.

    This tool should be used for all WhatsApp-approved template messages,
    including:
    - Daily / Monthly DGR reports
    - Transactional updates
    - Media-based templates (PDF, image, video)
    - Structured notifications with placeholders

    The caller is responsible for providing template components
    in the exact order defined in WhatsApp Template Manager.

    Args:
        to (str):
            Recipient WhatsApp number in international format.
            Example: "919876543210"

        template_name (str):
            Name of the approved WhatsApp template.
            Example: "wind_dgr_new"

        language_code (str, optional):
            Language code configured for the template.
            Example: "en_US"
            Defaults to "en_US".

        components (list[dict], optional):
            Template components payload as defined by WhatsApp.
            Can include header, body, footer, buttons, and media.

            Example:
            [
                {
                    "type": "header",
                    "parameters": [
                        { "type": "text", "text": "Customer Name" }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        { "type": "text", "text": "12543 kWh" },
                        { "type": "text", "text": "6.8 m/s" },
                        { "type": "text", "text": "02-Sep-2025" }
                    ]
                }
            ]

    Returns:
        dict[str, Any]:
            Raw WhatsApp Cloud API response including message ID,
            contact WA ID, and status metadata.

    Raises:
        McpError:
            If template structure is invalid, credentials are missing,
            or WhatsApp API returns an error.
    """
    client = get_whatsapp_client()
    return await client.send_template(
        to=to,
        template_name=template_name,
        language_code=language_code,
        components=components,
    )



@mcp.tool
async def send_whatsapp_service_options_menu(
    to: str,
    header_text: str,
    body_text: str,
    footer_text: str,
    button_text: str,
    sections: List[Dict[str, Any]],
) -> dict[str, Any]:
    """
    Send an interactive WhatsApp list menu with selectable service options.

    This tool should be used to present users with multiple selectable
    actions such as:
    - Demo workflows
    - Service catalogs
    - Support options
    - Navigation menus

    Args:
        to (str):
            Recipient WhatsApp number in international format.

        header_text (str):
            Title text displayed at the top of the menu.

        body_text (str):
            Main description text shown above the list.

        footer_text (str):
            Footer hint text displayed below the list.

        button_text (str):
            Text shown on the menu button (e.g., "Menu", "Options").

        sections (list[dict]):
            List sections as defined by WhatsApp.
            Each section contains rows with `id`, `title`, and `description`.

    Returns:
        dict[str, Any]:
            WhatsApp API response containing message ID and metadata.
    """
    client = get_whatsapp_client()
    return await client.send_interactive_list(
        to=to,
        header_text=header_text,
        body_text=body_text,
        footer_text=footer_text,
        button_text=button_text,
        sections=sections,
    )




@mcp.tool
async def send_whatsapp_confirmation_buttons(
    to: str,
    message: str,
    footer_text: str = "Once confirmed, you cannot undo. Use with caution 🚨",
) -> dict[str, Any]:
    """
    Send an interactive WhatsApp confirmation message with action buttons.

    This tool is intended for:
    - Confirm / Cancel workflows
    - Approval flows
    - Destructive or irreversible actions

    Args:
        to (str):
            Recipient WhatsApp number in international format.

        message (str):
            Main confirmation message displayed to the user.

        footer_text (str, optional):
            Warning or instruction text shown below the message.

    Returns:
        dict[str, Any]:
            WhatsApp API response including message ID and status metadata.
    """
    buttons = [
        {
            "type": "reply",
            "reply": {
                "id": "btn_confirmation",
                "title": "Confirmation",
            },
        },
        {
            "type": "reply",
            "reply": {
                "id": "btn_edit",
                "title": "Edit",
            },
        },
    ]

    client = get_whatsapp_client()
    return await client.send_interactive_buttons(
        to=to,
        body_text=message,
        footer_text=footer_text,
        buttons=buttons,
    )




@mcp.tool
async def send_whatsapp_document(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    filename: Optional[str] = None,
    caption: Optional[str] = None,
) -> dict[str, Any]:
    """
    Send a document (PDF or supported media) to a WhatsApp user.

    This tool supports BOTH WhatsApp document delivery modes:
    1. Uploaded media (media_id)  ← RECOMMENDED
    2. Publicly hosted URL (link)

    Exactly ONE of `media_id` or `link` must be provided.

    Args:
        to (str):
            Recipient WhatsApp number in E.164 format.
            Example: "919876543210"

        media_id (Optional[str]):
            WhatsApp Media ID returned from `upload_whatsapp_media`.
            Use this for PDFs uploaded to WhatsApp.

        link (Optional[str]):
            Public HTTPS URL of the document.
            Not recommended for sensitive or large files.

        filename (Optional[str]):
            Display name shown in WhatsApp chat.
            Example: "Wind_DGR_22_Dec_2025.pdf"

        caption (Optional[str]):
            Optional text shown below the document.

    Returns:
        dict:
            WhatsApp Cloud API response payload

    Raises:
        McpError:
            If neither or both media_id and link are provided.
    """

    if bool(media_id) == bool(link):
        raise McpError(
            ErrorData(
                code=400,
                message="Provide exactly ONE of media_id or link"
            )
        )

    client = get_whatsapp_client()

    return await client.send_document(
        to=to,
        media_id=media_id,
        link=link,
        filename=filename,
        caption=caption,
    )





@mcp.tool
async def send_whatsapp_flow(
    to: str,
    flow_id: str,
    body_text: str,
    cta_text: str,
    flow_token:str,
    start_screen: str,
    ) -> dict[str, Any]:
    """
    Send an interactive WhatsApp Flow to collect structured user data.

    This tool is ideal for:
    - Date / time / location collection
    - Form-based onboarding
    - Astrology / horoscope data intake
    - Any multi-step WhatsApp form flow

    Args:
        to (str): Recipient WhatsApp number in E.164 format
        flow_id (str): Approved WhatsApp Flow ID
        body_text (str): Main message text displayed to the user
        cta_text (str): Call-to-action text displayed as a button
        flow_token (str): Flow token obtained from the user
        start_screen (str): Start screen ID of the flow

    Returns:
        dict: WhatsApp Cloud API response
    """

    client = get_whatsapp_client()

    return await client.send_flow(
        to=to,
        flow_id=flow_id,
        body_text=body_text,
        cta_text=cta_text,
        flow_token=flow_token,
        start_screen=start_screen,
    )




@mcp.tool
async def send_whatsapp_image(
    to: str,
    media_id: Optional[str] = None,
    link: Optional[str] = None,
    caption: Optional[str] = None,
) -> dict[str, Any]:
    """
    Send an image to a WhatsApp user.

    Supports uploaded media (recommended) or publicly hosted image URLs.

    Exactly ONE of `media_id` or `link` must be provided.

    Args:
        to (str): Recipient WhatsApp number in E.164 format (e.g., "919876543210")
        media_id (Optional[str]): WhatsApp uploaded media ID
        link (Optional[str]): Public image URL (HTTPS)
        caption (Optional[str]): Optional caption text to show under the image

    Returns:
        dict: WhatsApp Cloud API response
    """

    if bool(media_id) == bool(link):
        raise McpError(
            ErrorData(
                code=400,
                message="Provide exactly ONE of media_id or link"
            )
        )

    client = get_whatsapp_client()
    return await client.send_image(
        to=to,
        media_id=media_id,
        link=link,
        caption=caption,
    )



# ---------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print("🚀 WhatsApp MCP Server running on port 2001")
    mcp.run(transport="streamable-http", port=2001)
