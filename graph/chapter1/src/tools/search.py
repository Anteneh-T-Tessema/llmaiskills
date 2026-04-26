from langchain_core.messages import ToolMessage
from src.config import get_search_tool
from src.graph.state import AgentState

search_tool = get_search_tool()

def tool_node(state: AgentState):
    """
    Executes tool calls from the agents.
    """
    if not search_tool:
        return {"messages": []}
        
    messages = state['messages']
    last_message = messages[-1]
    
    if not last_message.tool_calls:
        return {"messages": []}
        
    tool_outputs = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        # Standardize tool name check if needed
        if "tavily" in tool_name.lower() or "search" in tool_name.lower():
            result = search_tool.invoke(tool_call["args"])
            tool_outputs.append(
                ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=str(result),
                )
            )
    return {"messages": tool_outputs}
