import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

class SaaSwGateway:
    """A production-grade Gateway for managing multiple MCP nodes."""
    
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self.sessions = {}
        self.exit_stack = AsyncExitStack()

    async def connect_all(self):
        """Initializes connections to all nodes defined in the registry."""
        with open(self.registry_path, "r") as f:
            config = json.load(f)
        
        for name, params in config["mcpServers"].items():
            print(f"🔗 Connecting to node: {name}...")
            
            # Resolve absolute path for the server script
            script_path = os.path.abspath(params["args"][0])
            
            server_params = StdioServerParameters(
                command=params["command"],
                args=[script_path],
                env={**os.environ, **params.get("env", {})}
            )
            
            transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            session = await self.exit_stack.enter_async_context(ClientSession(transport[0], transport[1]))
            await session.initialize()
            
            self.sessions[name] = session
            print(f"✅ Node '{name}' is online.")

    async def list_global_tools(self):
        """Aggregates all tools from all connected nodes."""
        all_tools = {}
        for node_name, session in self.sessions.items():
            tools = await session.list_tools()
            for tool in tools.tools:
                all_tools[tool.name] = {"node": node_name, "tool": tool}
        return all_tools

    async def call_node_tool(self, tool_name: str, arguments: dict):
        """Routes a tool call to the correct node."""
        tools = await self.list_global_tools()
        if tool_name not in tools:
            raise ValueError(f"Tool {tool_name} not found in the Mesh.")
        
        node_name = tools[tool_name]["node"]
        return await self.sessions[node_name].call_tool(tool_name, arguments)

    async def __aenter__(self):
        await self.connect_all()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()
        print("\n🛑 Gateway shut down. All nodes disconnected.")

async def demo_gateway():
    registry = os.path.join(os.path.dirname(__file__), "config", "registry.json")
    async with SaaSwGateway(registry) as gateway:
        tools = await gateway.list_global_tools()
        print(f"\n📡 Total Discovered Tools: {list(tools.keys())}")
        
        # Call a specific node
        print("\n⚡️ Calling Market Sentiment Node...")
        result = await gateway.call_node_tool("get_market_sentiment", {"industry": "AI"})
        print(f"📊 Market Analysis Result:\n{json.dumps(result.content[0].text, indent=2)}")

if __name__ == "__main__":
    asyncio.run(demo_gateway())
