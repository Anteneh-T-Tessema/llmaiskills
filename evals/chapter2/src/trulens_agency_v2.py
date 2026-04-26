import os
import sys
from pathlib import Path

# Disable OTEL for local recording
os.environ["TRULENS_OTEL_TRACING"] = "0"

# Add the CrewAI Chapter 2 project to sys.path
project_root = Path(__file__).parent.parent.parent.parent
crew_path = str(project_root / "crewAI" / "chapter2")
if crew_path not in sys.path:
    sys.path.append(crew_path)

from trulens.core import TruSession, Metric, Select
from trulens.apps.basic import TruBasicApp
from trulens.providers.langchain import Langchain
from langchain_openai import ChatOpenAI

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

# Relevance: Answer vs User Input
f_relevance = Metric(
    name="Output Relevance", 
    implementation=provider.relevance_with_cot_reasons
).on_input().on(Select.RecordOutput[1]) # answer is at index 1

# Groundedness: Answer vs Research Context
f_groundedness = Metric(
    name="Groundedness",
    implementation=provider.groundedness_measure_with_cot_reasons
).on(Select.RecordOutput[0]).on(Select.RecordOutput[1]) # context at 0, answer at 1

# Safety Metrics
f_harmfulness = Metric(
    name="Harmfulness",
    implementation=provider.harmfulness_with_cot_reasons
).on(Select.RecordOutput[1])

feedbacks = [f_relevance, f_groundedness, f_harmfulness]

# 5. Import the actual system
try:
    from src.crew import run_agency
except ImportError as e:
    print(f"❌ Error: Could not import run_agency from Chapter 2.")
    print(f"Details: {e}")
    sys.exit(1)

# 6. Instrument the App
def run_agency_tuple(topic):
    res = run_agency(topic)
    return res['context'], res['answer']

tru_app = TruBasicApp(
    run_agency_tuple, 
    app_name='CrewAI_Agency_V2', 
    app_id='Agency_v2_FactChecker', 
    feedbacks=feedbacks,
    selectors_check_warning=True
)

# 7. Run Evaluations
print("🚀 Running TruLens Evaluation on Chapter 2 Agency (with Fact Checker)...")

topics = [
    "The ethical implications of autonomous AI auditing"
]

for topic in topics:
    print(f"❓ Topic: {topic}")
    with tru_app as recording:
        # returns {"answer": ..., "context": ...}
        response = tru_app.app(topic)
        
        if recording.records:
            record = recording.records[0]
            # Synchronously run feedback
            tru.run_feedback_functions(record=record, feedback_functions=feedbacks, wait=True)
            
    print(f"✅ Agency V2 Output Captured.\n")

# 8. Display Results
print("\n📊 TRULENS PERFORMANCE REPORT (V2)")
print("="*60)

records, feedback = tru.get_records_and_feedback(app_name=tru_app.app_name)

# Select columns to display
# Note: TruLens 1.0 feedback column names might match the Metric names
display_cols = ['input', 'answer'] + feedback
# Extract 'answer' from the output tuple for cleaner display
if not records.empty and 'output' in records.columns:
    records['answer'] = records['output'].apply(lambda x: str(x[1])[:200] + "...")

existing_cols = [c for c in display_cols if c in records.columns]

if records.empty:
    print("⚠️ No records found.")
else:
    print(records[existing_cols])

print(f"\n💡 Tip: Compare 'Groundedness' scores with Chapter 1 in the dashboard!")
