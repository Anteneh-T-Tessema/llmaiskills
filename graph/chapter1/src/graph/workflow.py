from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.agents.researcher import researcher_node
from src.agents.editor import editor_node
from src.tools.search import tool_node

def should_continue(state: AgentState):
    """
    Check if tools need to be called or if we go to editor.
    """
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return "editor"

def editor_critique(state: AgentState):
    """
    Check if the editor is finished.
    """
    last_message = state['messages'][-1]
    if "final summary" in last_message.content.lower():
        return "end"
    return "researcher"

def create_workflow():
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("editor", editor_node)
    
    # Set Entry Point
    workflow.set_entry_point("researcher")
    
    # Add Edges
    workflow.add_conditional_edges(
        "researcher",
        should_continue,
        {
            "tools": "tools",
            "editor": "editor",
        }
    )
    
    workflow.add_edge("tools", "researcher")
    
    workflow.add_conditional_edges(
        "editor",
        editor_critique,
        {
            "researcher": "researcher",
            "end": END,
        }
    )
    
    return workflow.compile()
