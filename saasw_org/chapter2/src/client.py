import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    # Dynamically find the absolute path to server.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "server.py")

    # 1. Define how to connect to the server
    server_params = StdioServerParameters(
        command="/usr/local/bin/python3.12",
        args=[server_path],
    )

    print("🚀 Connecting to MCP Server...")
    
    # 2. Establish the connection
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 3. Initialize the session
            await session.initialize()
            print("✅ Connected!")

            # 4. List available tools
            tools = await session.list_tools()
            print(f"\nAvailable Tools: {[t.name for t in tools.tools]}")

            # 5. Call a tool
            print("\nCalling 'get_current_time'...")
            result = await session.call_tool("get_current_time", arguments={})
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_client())
