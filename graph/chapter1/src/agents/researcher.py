from langchain_core.messages import HumanMessage
from src.config import get_llm, get_search_tool
from src.graph.state import AgentState

# Initialize LLM and bind tools
llm = get_llm()
search_tool = get_search_tool()
tools = [search_tool] if search_tool else []
llm_with_tools = llm.bind_tools(tools) if tools else llm

def researcher_node(state: AgentState):
    """
    The Researcher node calls the search tool to gather information.
    """
    messages = state['messages']
    
    # Add a system instruction if it's the start
    if len(messages) == 1:
        prompt = """You are a world-class researcher. Search for the latest and most relevant info on the topic. 
        If tools are available, use them to gather data. 
        If tools are not available or fail, provide a deep logical analysis based on your internal knowledge.
        Your output must be a comprehensive research report, never raw JSON or tool-call placeholders."""
        messages = [HumanMessage(content=prompt)] + list(messages)
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
