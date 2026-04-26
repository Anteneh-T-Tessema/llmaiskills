from langchain_core.messages import HumanMessage
from src.config import get_llm
from src.graph.state import AgentState

llm = get_llm()

def editor_node(state: AgentState):
    """
    The Editor reviews the researcher's work and provides a final summary.
    """
    messages = state['messages']
    review_prompt = (
        "You are a Senior Editor. Review the research findings. "
        "If they are sufficient, provide a polished 'FINAL SUMMARY'. "
        "If something is missing, explain exactly what needs more research."
    )
    
    response = llm.invoke([HumanMessage(content=review_prompt)] + messages)
    return {"messages": [response]}
