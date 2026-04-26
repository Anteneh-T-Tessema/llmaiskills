import os
os.environ["TRULENS_OTEL_TRACING"] = "0"
from trulens.core import TruSession, Metric
from trulens.apps.basic import TruBasicApp
from trulens.providers.langchain import Langchain
from langchain_openai import ChatOpenAI
import pandas as pd

# 1. Setup local LLM
# We use llama3.1 via Ollama's OpenAI-compatible API
llm = ChatOpenAI(
    model="llama3.1",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0,
)

# 2. Initialize TruLens Session
tru = TruSession()
tru.reset_database()

# 3. Setup Feedback Provider
# We wrap the LangChain LLM to use it for scoring
provider = Langchain(chain=llm)

# 4. Define Feedback Functions
# relevance() measures how relevant the answer is to the question
f_relevance = Metric(name="Relevance", implementation=provider.relevance_with_cot_reasons).on_input().on_output()

# 5. Define the App Logic
def sovereign_ai_app(question: str):
    """
    A mock RAG app that returns a hardcoded answer for testing.
    """
    knowledge_base = {
        "What are the core requirements for Sovereign AI?": "Sovereign AI requires decentralization, autonomous auditing, and self-improvement loops.",
        "What is the role of decentralized nodes?": "Decentralized nodes ensure that no single entity has control over the AI's execution or data.",
    }
    return knowledge_base.get(question, "I don't have information on that topic in my sovereign knowledge base.")

# 6. Instrument the App
# We use TruBasicApp to wrap a simple function
tru_app = TruBasicApp(sovereign_ai_app, app_name='SovereignAI', app_id='SovereignAI_v1', feedbacks=[f_relevance])

# 7. Run Evaluations
print("🚀 Running TrueLens v1.0 Evaluations...")
questions = [
    "What are the core requirements for Sovereign AI?",
    "What is the role of decentralized nodes?",
    "What is the weather in New York?" # Irrelevant question to test relevance score
]

records_to_wait = []
for q in questions:
    print(f"❓ Question: {q}")
    with tru_app as recording:
        response = tru_app.app(q)
        record = recording.records[0]
        records_to_wait.append(record)
        # Manually trigger feedback
        tru.run_feedback_functions(record=record, feedback_functions=[f_relevance], wait=False)
    print(f"✅ Response: {response}\n")

# 8. Display Results
print("📊 TRULENS PERFORMANCE REPORT")
print("="*60)

import time

# ... (previous code)

# Wait for feedback to complete
print("⏳ Waiting for feedback scoring to finish (15s)...")
import time
time.sleep(15)

records, feedback = tru.get_records_and_feedback()

# Handle potentially renamed columns or missing feedback
display_cols = ['input', 'output'] + feedback
# Filter columns that actually exist in the dataframe
existing_cols = [c for c in display_cols if c in records.columns]

if records.empty:
    print("⚠️ No records found for this app.")
else:
    print(records[existing_cols])

print("\n💡 Tip: Run 'tru.run_dashboard()' in a notebook to see the full UI.")
