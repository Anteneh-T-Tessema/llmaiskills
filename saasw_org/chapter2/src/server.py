import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# 1. Initialize the Low-Level Server
server = Server("Time-Weather-Node")

# 2. Register a Tool (Low-level manual way)
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_current_time",
            description="Get the current system time.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Execute a tool call."""
    if name == "get_current_time":
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [types.TextContent(type="text", text=f"The current time is: {current_time}")]
    
    raise ValueError(f"Tool not found: {name}")

async def main():
    # 3. Run the server using Standard I/O
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
