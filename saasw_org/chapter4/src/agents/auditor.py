from crewai import Agent
from src.tools.mcp_bridge import currency_converter, roi_calculator

def create_auditor_agent():
    return Agent(
        role="Senior Financial Auditor",
        goal="Audit project finances and calculate growth metrics using the MCP Finance Node.",
        backstory=(
            "You are a precision-oriented auditor. You don't guess—you use "
            "the decentralized Finance Node to get exact ROI and currency data."
        ),
        tools=[currency_converter, roi_calculator],
        verbose=True,
        allow_delegation=False, 
        max_iter=3,
        llm="ollama/llama3.2" 
    )
