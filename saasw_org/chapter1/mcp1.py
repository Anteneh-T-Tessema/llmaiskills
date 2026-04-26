import json
import os
from fastmcp import FastMCP
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# 1. Initialize the server
mcp = FastMCP("SaaSw-Core-Node")

PROJECTS_FILE = os.path.join(os.path.dirname(__file__), "projects.json")
search_wrapper = DuckDuckGoSearchAPIWrapper()

# Helper to manage state
def load_projects():
    if not os.path.exists(PROJECTS_FILE):
        return []
    with open(PROJECTS_FILE, "r") as f:
        return json.load(f)

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=2)

# --- TOOLS ---

@mcp.tool()
def calculate_growth(initial_value: float, rate: float, years: int) -> str:
    """Calculates compound interest for market projections."""
    final_amount = initial_value * (1 + rate)**years
    return f"After {years} years, the value will be {final_amount:.2f}"

@mcp.tool()
def register_project(name: str, objective: str) -> str:
    """Registers a new SaaSw project into the persistent registry."""
    projects = load_projects()
    projects.append({"name": name, "objective": objective})
    save_projects(projects)
    return f"Project '{name}' successfully registered in the SaaSw Node."

@mcp.tool()
def list_projects() -> str:
    """Lists all active projects registered in this SaaSw Node."""
    projects = load_projects()
    if not projects:
        return "No projects currently registered."
    
    output = "Active SaaSw Projects:\n"
    for p in projects:
        output += f"- {p['name']}: {p['objective']}\n"
    return output

@mcp.tool()
def get_market_intelligence(topic: str) -> str:
    """
    Performs real-time web research on a given topic to gather market intelligence.
    
    Args:
        topic: The market or technology trend to research.
    """
    try:
        results = search_wrapper.run(topic)
        return f"Market Intelligence for '{topic}':\n\n{results}"
    except Exception as e:
        return f"Error gathering intelligence for '{topic}': {str(e)}"

# --- RESOURCES ---

@mcp.resource("info://manifesto")
def get_manifesto() -> str:
    """Returns the core definition of Service-as-a-Software."""
    return "SaaSw: The evolution of software into autonomous, deterministic service endpoints."

@mcp.resource("info://projects")
def get_projects_resource() -> str:
    """Returns the raw project list as a resource."""
    return json.dumps(load_projects(), indent=2)

if __name__ == "__main__":
    mcp.run()
