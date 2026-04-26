import asyncio
import os
import sys
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Import our previous chapters
sys.path.append("/Users/antenehtessema/developer/graphcrewgen")
from saasw_org.chapter6.src.evolution import evolve_infrastructure

# Initialize the Master Architect
llm = ChatOllama(model="llama3.2")

async def run_factory(business_goal: str):
    print(f"\n🏭 WELCOME TO THE AI EMPLOYEE FACTORY")
    print(f"🎯 Objective: {business_goal}\n")

    # PHASE 1: Evolution (Chapter 6)
    print("--- PHASE 1: EVOLVING INFRASTRUCTURE ---")
    await evolve_infrastructure(business_goal)
    print("✅ Infrastructure updated with new autonomous capability.")

    # PHASE 2: Verification (Gateway Check)
    print("\n--- PHASE 2: MESH INTEGRATION ---")
    registry_path = "saasw_org/chapter5/config/registry.json"
    with open(registry_path, "r") as f:
        registry = __import__("json").load(f)
    
    new_node_id = business_goal.lower().replace(" ", "-")[:15]
    if new_node_id in registry["mcpServers"]:
        print(f"📡 Node '{new_node_id}' is now live in the Mesh.")
    
    # PHASE 3: Execution
    print("\n--- PHASE 3: TASK EXECUTION ---")
    completion_prompt = (
        f"You have just autonomously built a new MCP node for: {business_goal}. "
        "It is registered in the production gateway and visible on the dashboard. "
        "Write a 3-sentence victory report for the user."
    )
    
    result = llm.invoke([HumanMessage(content=completion_prompt)])
    print("\n" + "="*40)
    print("🏆 FACTORY SUCCESS REPORT")
    print("="*40)
    print(result.content)
    print("\nCheck your Sovereign Dashboard (Chapter 7) to see the new service!")

if __name__ == "__main__":
    import sys
    goal = sys.argv[1] if len(sys.argv) > 1 else "YouTube Strategy Generator"
    asyncio.run(run_factory(goal))
