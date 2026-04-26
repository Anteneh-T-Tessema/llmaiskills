import json
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 1. Setup the Model Client (Using our local Ollama)
model_client = OpenAIChatCompletionClient(
    model="llama3.2",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model_info={"vision": False, "function_calling": True, "json_output": False, "family": "llama3"}
)

async def evolve_infrastructure(requirement: str):
    print(f"🧬 Starting Autonomous Evolution: {requirement}")
    
    # 2. Define the Developer Agent
    developer = AssistantAgent(
        name="Node_Developer",
        model_client=model_client,
        system_message=(
            "You are an expert MCP Node Developer. Your task is to write a Python script "
            "using FastMCP that fulfills the user requirement. "
            "Output ONLY the complete Python code for the node. "
            "Save the file to 'saasw_org/chapter5/nodes/generated_node.py'."
        )
    )

    print("✍️  Agent is writing the new Service Node...")
    
    generated_code = f"""
from fastmcp import FastMCP
import math

mcp = FastMCP("Autonomous-Requirement-Node")

@mcp.tool()
def calculate_metric(value: float) -> str:
    \"\"\"Calculates a complex metric based on: {requirement}\"\"\"
    result = math.sqrt(value) * 1.5 # Mock logic
    return f"Autonomous calculation result: {{result}}"

if __name__ == "__main__":
    mcp.run()
"""

    node_path = "saasw_org/chapter5/nodes/generated_node.py"
    # Ensure directory exists
    os.makedirs(os.path.dirname(node_path), exist_ok=True)
    
    with open(node_path, "w") as f:
        f.write(generated_code)
    print(f"✅ Node written to: {node_path}")

    # 4. The Integrator Step: Update the Production Registry
    registry_path = "saasw_org/chapter5/config/registry.json"
    with open(registry_path, "r") as f:
        registry = json.load(f)
    
    node_id = requirement.lower().replace(" ", "-")[:15]
    registry["mcpServers"][node_id] = {
        "command": "/usr/local/bin/python3.12",
        "args": [node_path],
        "env": {"GENERATED_BY": "AutoGen-Evolution-Loop"}
    }

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=4)
    
    print(f"🚀 Registry updated! New node '{node_id}' is now part of the Organization.")

if __name__ == "__main__":
    import sys
    req = sys.argv[1] if len(sys.argv) > 1 else "Metric calculation service"
    asyncio.run(evolve_infrastructure(req))
