import sys
from langchain_core.messages import HumanMessage
from src.graph.workflow import create_workflow

def run_system(query: str):
    app = create_workflow()
    inputs = {"messages": [HumanMessage(content=query)]}
    
    print(f"\n--- Starting Research for: {query} ---\n")
    
    for output in app.stream(inputs):
        for node_name, state_update in output.items():
            print(f"[{node_name}]")
            message = state_update["messages"][-1]
            content = message.content if hasattr(message, 'content') else str(message)
            # Truncate for visibility
            display_content = content[:300] + ("..." if len(content) > 300 else "")
            print(f"{display_content}\n")
            print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "What are the latest developments in generative AI for coding?"
    
    run_system(query)
