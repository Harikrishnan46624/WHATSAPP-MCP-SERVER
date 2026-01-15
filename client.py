import asyncio
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    load_dotenv()

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    api_token = os.getenv("MCP_API_TOKEN")
    
    # WhatsApp credentials from .env (same as your weather server)
    whatsapp_phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    whatsapp_access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    whatsapp_api_version = os.getenv("WHATSAPP_API_VERSION", "v18.0")

    client = MultiServerMCPClient(
        {
            # Your existing weather server
            "weather": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:2000/mcp",
                "headers": {
                    "Authorization": f"Bearer {api_token}",
                    "X-Custom-Header": "custom-value",
                },
            },
            # NEW: WhatsApp server (same port, different server name)
            "whatsapp": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:2000/mcp",  # Same server, different MCP name
                "headers": {
                    "Authorization": f"Bearer {api_token}",
                    # WhatsApp credentials passed via custom headers
                    "x-whatsapp-auth": f"Bearer {whatsapp_phone_number_id}",
                    "x-whatsapp-creds": f"Bearer {whatsapp_access_token}:{whatsapp_api_version}",
                },
            }
        }
    )

    tools = await client.get_tools()
    print("Available tools:", [tool.name for tool in tools])  # See both weather + send_whatsapp_text
    agent = create_agent("openai:gpt-4.1", tools)
    # Test WhatsApp tool
    response = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "Send a WhatsApp message to 919876543210 saying 'Hello from LangChain MCP agent!'"}
            ]
        }
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
