import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    State representing the conversation history.
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]
