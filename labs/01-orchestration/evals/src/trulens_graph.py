import os
import sys
from pathlib import Path

# Disable OTEL for local recording
os.environ["TRULENS_OTEL_TRACING"] = "0"

# Add the LangGraph project to sys.path
project_root = Path(__file__).parent.parent.parent.parent
graph_path = str(project_root / "graph" / "chapter1")
if graph_path not in sys.path:
    sys.path.append(graph_path)

from trulens.core import TruSession, Metric
from trulens.apps.basic import TruBasicApp
from trulens.providers.langchain import Langchain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 1. Setup local LLM for evaluation
llm = ChatOpenAI(
    model="llama3.1",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0,
)

# 2. Initialize TruLens Session
tru = TruSession()

# 3. Setup Feedback Provider
provider = Langchain(chain=llm)

# 4. Define Feedback Functions
f_relevance = Metric(
    name="Output Relevance", 
    implementation=provider.relevance_with_cot_reasons
).on_input().on_output()

# Safety Metrics
f_harmfulness = Metric(
    name="Harmfulness",
    implementation=provider.harmfulness_with_cot_reasons
).on_output()

f_maliciousness = Metric(
    name="Maliciousness",
    implementation=provider.maliciousness_with_cot_reasons
).on_output()

f_hate = Metric(
    name="Hate Speech",
    implementation=provider.hate_with_cot_reasons
).on_output()

feedbacks = [f_relevance, f_harmfulness, f_maliciousness, f_hate]

# 5. Import the actual system
try:
    from src.graph.workflow import create_workflow
except ImportError as e:
    print(f"❌ Error: Could not import create_workflow. Make sure {graph_path} is correct.")
    print(f"Details: {e}")
    sys.exit(1)

# 6. Define Wrapper Function for LangGraph
# TruBasicApp works best with a simple function that returns the final string
def run_research_graph(query: str):
    """
    Wrapper to execute the LangGraph research workflow and return the final answer.
    """
    app = create_workflow()
    inputs = {"messages": [HumanMessage(content=query)]}
    
    # We use invoke to get the final state of the graph
    result = app.invoke(inputs)
    
    # The last message in the state should be the final summary from the editor
    final_message = result["messages"][-1]
    return final_message.content if hasattr(final_message, 'content') else str(final_message)

# 7. Instrument the App
tru_app = TruBasicApp(
    run_research_graph, 
    app_name='LangGraph_Research', 
    app_id='Graph_v1', 
    feedbacks=feedbacks
)

# 8. Run Evaluation
print("🚀 Running TruLens Evaluation on LangGraph Research System...")

queries = [
    "What are the latest developments in generative AI for coding?"
]

for query in queries:
    print(f"❓ Query: {query}")
    with tru_app as recording:
        # Trigger the LangGraph workflow
        response = tru_app.app(query)
        
        # Access the record from the context
        if recording.records:
            record = recording.records[0]
            # Synchronously run feedback
            tru.run_feedback_functions(record=record, feedback_functions=feedbacks, wait=True)
            
    print(f"✅ Graph Execution Captured.\n")

# 9. Display Results
print("\n📊 TRULENS PERFORMANCE REPORT")
print("="*60)

# Fetch records for this app
records, feedback = tru.get_records_and_feedback(app_name=tru_app.app_name)

print(f"DEBUG: Feedback columns found: {feedback}")

# Filter and display relevant columns
display_cols = ['input', 'output'] + feedback
existing_cols = [c for c in display_cols if c in records.columns]

if records.empty:
    print("⚠️ No records found for this app.")
else:
    # Truncate output for cleaner display
    records['output'] = records['output'].apply(lambda x: str(x)[:200] + "...")
    print(records[existing_cols])

print(f"\n💡 Tip: Run 'tru.run_dashboard()' to see the full traces and reasoning.")
