import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. Initialize the LLM (Host Intelligence)
# Using llama3.2 as it is significantly faster for local testing
llm = ChatOllama(model="llama3.2")

async def run_host(user_query: str):
    # Dynamically find the absolute path to server.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "server.py")

    server_params = StdioServerParameters(
        command="/usr/local/bin/python3.12",
        args=[server_path],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. Get tools from the server
            mcp_tools = await session.list_tools()
            tool_names = [t.name for t in mcp_tools.tools]
            print(f"🔍 Host discovered tools: {tool_names}")
            
            # 3. Strict Host Logic: 
            print(f"🧠 Asking LLM to process query: '{user_query}'")
            prompt = (
                f"SYSTEM: You are a helpful assistant with access to these tools: {tool_names}.\n"
                "CRITICAL RULE: If the user asks for the time, you MUST respond with exactly 'get_current_time'. "
                "DO NOT guess the time. DO NOT provide a conversational response. "
                "ONLY output the tool name if a tool can help. "
                f"\n\nUser Question: {user_query}"
            )
            
            response = llm.invoke([HumanMessage(content=prompt)])
            decision = response.content.strip().lower()
            print(f"💭 LLM Decision: '{decision}'")

            if "get_current_time" in decision:
                # 4. Execute the decision via the Client
                print("🛠  Calling server tool: get_current_time...")
                result = await session.call_tool("get_current_time", arguments={})
                tool_output = result.content[0].text
                print(f"📥 Server Response: {tool_output}")
                
                # 5. Final Natural Language response
                print("✍️  Asking LLM to summarize the result...")
                final_response = llm.invoke([
                    HumanMessage(content=user_query),
                    HumanMessage(content=f"Tool Output: {tool_output}. Briefly summarize this for the user.")
                ])
                print(f"\n🤖 Host Final Answer: {final_response.content}")
            else:
                print(f"\n🤖 Host Direct Answer: {response.content}")

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "What time is it?"
    asyncio.run(run_host(query))
