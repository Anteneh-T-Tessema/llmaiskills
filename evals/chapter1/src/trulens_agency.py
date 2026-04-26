import os
import sys
from pathlib import Path

# Disable OTEL for local recording
os.environ["TRULENS_OTEL_TRACING"] = "0"

# Add the CrewAI project to sys.path
# This ensures we can import 'src' from the crewAI/chapter1 directory
project_root = Path(__file__).parent.parent.parent.parent
crew_path = str(project_root / "crewAI" / "chapter1")
if crew_path not in sys.path:
    sys.path.append(crew_path)

from trulens.core import TruSession, Metric
from trulens.apps.basic import TruBasicApp
from trulens.providers.langchain import Langchain
from langchain_openai import ChatOpenAI

# 1. Setup local LLM for evaluation
# We use llama3.1 via Ollama
llm = ChatOpenAI(
    model="llama3.1",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0,
)

# 2. Initialize TruLens Session
tru = TruSession()
# tru.reset_database() # Uncomment if you want a clean slate

# 3. Setup Feedback Provider
provider = Langchain(chain=llm)

# 4. Define Feedback Functions
f_relevance = Metric(
    name="Output Relevance", 
    implementation=provider.relevance_with_cot_reasons
).on_input().on_output()

f_coherence = Metric(
    name="Coherence",
    implementation=provider.coherence_with_cot_reasons
).on_output()

f_conciseness = Metric(
    name="Conciseness",
    implementation=provider.conciseness_with_cot_reasons
).on_output()

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

feedbacks = [f_relevance, f_coherence, f_conciseness, f_harmfulness, f_maliciousness, f_hate]

# 5. Import the actual system
try:
    from src.crew import run_agency
except ImportError as e:
    print(f"❌ Error: Could not import run_agency. Make sure {crew_path} is correct.")
    print(f"Details: {e}")
    sys.exit(1)

# 6. Instrument the App
# We wrap the CrewAI entry point 'run_agency'
tru_app = TruBasicApp(
    run_agency, 
    app_name='CrewAI_Agency', 
    app_id='Agency_v1', 
    feedbacks=feedbacks
)

# 7. Run Evaluations
print("🚀 Running TruLens Evaluation on CrewAI Agency...")

# We'll test with a specific topic
topics = [
    "The role of sovereign nodes in decentralized AI systems"
]

for topic in topics:
    print(f"❓ Topic: {topic}")
    with tru_app as recording:
        # This will trigger the full CrewAI workflow: Researcher -> Copywriter -> Editor
        response = tru_app.app(topic)
        
        # Access the record from the context
        if recording.records:
            record = recording.records[0]
            # Manually trigger feedback for reliability in this environment
            tru.run_feedback_functions(record=record, feedback_functions=feedbacks, wait=True)
            
    print(f"✅ Agency Output Captured.\n")

# 8. Display Results
print("\n📊 TRULENS PERFORMANCE REPORT")
print("="*60)
# print("⏳ Waiting for feedback scoring (15s)...")
# import time
# time.sleep(15)

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
