
from mcp import McpError
from mcp.types import ErrorData
import httpx
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------
# WHATSAPP CLIENT (CORE)
# ---------------------------------------------------------------------


class WhatsAppClient:
    """
    Reusable WhatsApp Cloud API client.
    """

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        api_version: str,
        timeout: float = 15.0,
    ):
        self.base_url = f"https://graph.facebook.com/{api_version}/{phone_number_id}"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    # ---------------- TEXT MESSAGE ---------------- #

    async def send_text(
        self,
        to: str,
        body: str,
        preview_url: bool = False,
    ) -> dict[str, Any]:

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": body,
                "preview_url": preview_url,
            },
        }

        return await self._post(payload)

    # ---------------- TEMPLATE MESSAGE ---------------- #

    async def send_template(
        self,
        to: str,
        template_name: str,
        language_code: str,
        components: Optional[List[Dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """
        Fully dynamic template sender.

        components example:
        [
          {
            "type": "header",
            "parameters": [
              {
                "type": "document",
                "document": { "id": "...", "filename": "file.pdf" }
              }
            ]
          },
          {
            "type": "body",
            "parameters": [
              { "type": "text", "text": "Customer" },
              { "type": "text", "text": "Plant" },
              { "type": "text", "text": "2025-09-01" }
            ]
          }
        ]
        """

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
            },
        }

        if components:
            payload["template"]["components"] = components

        return await self._post(payload)
    

    # ---------------- INTERACTIVE: LIST MENU ---------------- #

    async def send_interactive_list(
        self,
        to: str,
        header_text: str,
        body_text: str,
        footer_text: str,
        button_text: str,
        sections: List[Dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Send an interactive WhatsApp list menu.
        """

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": header_text,
                },
                "body": {
                    "text": body_text,
                },
                "footer": {
                    "text": footer_text,
                },
                "action": {
                    "button": button_text,
                    "sections": sections,
                },
            },
        }

        return await self._post(payload)

    # ---------------- INTERACTIVE: CONFIRMATION BUTTONS ---------------- #

    async def send_interactive_buttons(
        self,
        to: str,
        body_text: str,
        footer_text: str,
        buttons: List[Dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Send an interactive WhatsApp button message.
        """

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body_text,
                },
                "footer": {
                    "text": footer_text,
                },
                "action": {
                    "buttons": buttons,
                },
            },
        }

        return await self._post(payload)
    




    


    # ---------------- DOCUMENT MESSAGE ---------------- #
    async def send_document(
        self,
        to: str,
        media_id: Optional[str] = None,
        link: Optional[str] = None,
        filename: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send a document message via WhatsApp Cloud API.

        Exactly ONE of `media_id` or `link` must be provided.

        Args:
            to (str): Recipient WhatsApp number in E.164 format
            media_id (Optional[str]): Uploaded WhatsApp media ID
            link (Optional[str]): Public document URL
            filename (Optional[str]): Display filename
            caption (Optional[str]): Caption text

        Returns:
            dict: WhatsApp API response
        """

        document: Dict[str, Any] = {}

        if media_id:
            document["id"] = media_id
        elif link:
            document["link"] = link

        if filename:
            document["filename"] = filename

        if caption:
            document["caption"] = caption

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "document",
            "document": document,
        }

        return await self._post(payload)

    


    async def send_flow(
        self,
        to: str,
        flow_id: str,
        body_text: str,
        cta_text: str = "Share Details",
        flow_token: str = "data_collection_flow",
        start_screen: str = "RECOMMEND",
    ) -> dict[str, Any]:
        """
        Send a WhatsApp Interactive Flow message.

        Args:
            to (str): Recipient WhatsApp number (E.164 format)
            flow_id (str): WhatsApp Flow ID (approved)
            body_text (str): Message shown above the CTA
            cta_text (str): CTA button label
            flow_token (str): Arbitrary token to identify flow session
            start_screen (str): Initial screen ID in the flow

        Returns:
            dict: WhatsApp API response
        """

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "body": {"text": body_text},
                "footer": {"text": "Your details are safe with us 🔒"},
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_token": flow_token,
                        "flow_id": flow_id,
                        "flow_cta": cta_text,
                        "flow_action": "navigate",
                        "flow_action_payload": {
                            "screen": start_screen
                        }
                    }
                }
            }
        }

        return await self._post(payload)
    


    async def send_image(
        self,
        to: str,
        media_id: Optional[str] = None,
        link: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Send an image message via WhatsApp Cloud API.

        Args:
            to (str): Recipient WhatsApp number in E.164 format
            media_id (Optional[str]): Uploaded media ID
            link (Optional[str]): Public image URL
            caption (Optional[str]): Caption text

        Returns:
            dict: WhatsApp API response
        """

        image: Dict[str, Any] = {}
        if media_id:
            image["id"] = media_id
        elif link:
            image["link"] = link

        if caption:
            image["caption"] = caption

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": image,
        }

        return await self._post(payload)




    # ---------------- HTTP CORE ---------------- #

    async def _post(self, payload: Dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/messages"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, headers=self.headers, json=payload)

        if resp.status_code == 200:
            return resp.json()

        self._raise_error(resp)

    @staticmethod
    def _raise_error(resp: httpx.Response) -> None:
        try:
            error = resp.json().get("error", {})
            message = error.get("message", "Unknown WhatsApp API error")
        except Exception:
            message = resp.text or "Unknown WhatsApp API error"

        raise McpError(
            ErrorData(code=resp.status_code, message=f"WhatsApp API failed: {message}")
        )
