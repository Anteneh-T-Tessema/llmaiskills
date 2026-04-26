from crewai import Agent
from crewai.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from src.config import Config

# Define a custom tool for DuckDuckGo Search
class SearchTool:
    @tool("search_tool")
    def search(query: str):
        """Search the internet for a given topic and return relevant results."""
        return DuckDuckGoSearchAPIWrapper().run(query)

def create_researcher():
    return Agent(
        role='Expert Researcher',
        goal='Extract key insights and trending angles from a given {topic} or URL. If you use tools, summarize the results. If no tools are used, provide a deep logical analysis.',
        backstory='You are a master at finding the "hook" in any content. You scan the web and provide detailed, data-backed insights. IMPORTANT: Never output raw JSON for tool calls in your "Final Answer". If you need to use a tool, use it. Your final response must be a human-readable summary of your findings.',
        tools=[SearchTool().search],
        # Using the model name string with 'ollama/' prefix
        llm=f"ollama/{Config.OLLAMA_MODEL}",
        verbose=True,
        allow_delegation=False
    )
