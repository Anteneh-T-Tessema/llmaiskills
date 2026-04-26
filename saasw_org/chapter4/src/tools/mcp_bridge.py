import asyncio
import os
from crewai.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define the path to our Finance Node from Chapter 3
FINANCE_SERVER_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "chapter3", "src", "finance_server.py"
))

def run_mcp_tool_sync(tool_name: str, arguments: dict):
    """Helper to run async MCP calls in a synchronous CrewAI environment."""
    async def call():
        server_params = StdioServerParameters(
            command="/usr/local/bin/python3.12",
            args=[FINANCE_SERVER_PATH]
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text
    
    return asyncio.run(call())

@tool("currency_converter")
def currency_converter(amount: float, from_curr: str, to_curr: str) -> str:
    """
    Useful for converting currency. 
    Args: amount (float), from_curr (str), to_curr (str). 
    Example: amount=100, from_curr='USD', to_curr='EUR'
    """
    return run_mcp_tool_sync("convert_currency", {
        "amount": amount, 
        "from_curr": from_curr, 
        "to_curr": to_curr
    })

@tool("roi_calculator")
def roi_calculator(initial: float, final: float) -> str:
    """
    Useful for calculating ROI (Return on Investment).
    Args: initial (float), final (float).
    """
    return run_mcp_tool_sync("calculate_roi", {
        "initial": initial, 
        "final": final
    })
