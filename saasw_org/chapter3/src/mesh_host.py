import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

# Initialize the Brain
llm = ChatOllama(model="llama3.2")

async def run_mesh_host(user_query: str):
    # Dynamically find the server paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    finance_server = os.path.join(base_dir, "finance_server.py")
    system_server = os.path.join(base_dir, "system_server.py")

    # Define Server Parameters
    finance_params = StdioServerParameters(command="/usr/local/bin/python3.12", args=[finance_server])
    system_params = StdioServerParameters(command="/usr/local/bin/python3.12", args=[system_server])

    # We use AsyncExitStack to manage multiple simultaneous connections
    async with AsyncExitStack() as stack:
        print("🌐 Initializing Mesh Connection...")
        
        # Connect to Finance Node
        f_transport = await stack.enter_async_context(stdio_client(finance_params))
        f_session = await stack.enter_async_context(ClientSession(f_transport[0], f_transport[1]))
        await f_session.initialize()
        
        # Connect to System Node
        s_transport = await stack.enter_async_context(stdio_client(system_params))
        s_session = await stack.enter_async_context(ClientSession(s_transport[0], s_transport[1]))
        await s_session.initialize()

        # 1. Aggregate Tools from both nodes
        f_tools = await f_session.list_tools()
        s_tools = await s_session.list_tools()
        
        all_tool_names = [t.name for t in f_tools.tools] + [t.name for t in s_tools.tools]
        print(f"📡 Mesh Active. Discovered tools from all nodes: {all_tool_names}")

        # 2. Host Logic
        print(f"🧠 Processing user query: '{user_query}'")
        prompt = (
            f"You are a Mesh Orchestrator with access to these services: {all_tool_names}.\n"
            "If you need a tool, respond with ONLY the tool name.\n"
            f"User Request: {user_query}"
        )
        
        response = llm.invoke([HumanMessage(content=prompt)])
        decision = response.content.strip().lower()
        print(f"💭 Mesh Decision: '{decision}'")

        # 3. Route the call to the correct Node
        target_session = None
        if decision in [t.name for t in f_tools.tools]:
            print(f"💸 Routing to Finance-Node...")
            target_session = f_session
        elif decision in [t.name for t in s_tools.tools]:
            print(f"💻 Routing to System-Node...")
            target_session = s_session

        if target_session:
            # For simplicity, we'll use empty args or default args for this demo
            result = await target_session.call_tool(decision, arguments={})
            tool_output = result.content[0].text
            print(f"📥 Node Response: {tool_output}")
            
            # Final Summary
            final_resp = llm.invoke([
                HumanMessage(content=f"The tool {decision} returned: {tool_output}. Summarize this for the user query: {user_query}")
            ])
            print(f"\n🤖 Mesh Final Answer: {final_resp.content}")
        else:
            print(f"\n🤖 Direct Answer: {response.content}")

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "List my folders and convert 100 USD to EUR"
    asyncio.run(run_mesh_host(query))
