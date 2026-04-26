import sys
import os
from crew import AgenticRAGCrew

# Disable OTEL for clean local execution
os.environ["TRULENS_OTEL_TRACING"] = "0"

def run():
    """
    Run the Agentic RAG Agency.
    """
    print("🚀 Launching Agentic RAG Agency (Chapter 5)...")
    
    inputs = {
        'topic': 'The use of AI in sustainable agriculture'
    }
    
    try:
        result = AgenticRAGCrew().crew().kickoff(inputs=inputs)
        print("\n\n✅ FINAL AGENCY OUTPUT:")
        print("==================================================")
        print(result)
    except Exception as e:
        print(f"❌ Agency error: {e}")

if __name__ == "__main__":
    run()
