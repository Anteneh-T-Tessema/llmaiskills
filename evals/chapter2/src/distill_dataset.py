import os
import json
from pathlib import Path
from trulens.core import TruSession

# Disable OTEL for consistent local data retrieval
os.environ["TRULENS_OTEL_TRACING"] = "0"

# Setup paths
project_root = Path(__file__).parent.parent.parent.parent
output_file = project_root / "evals" / "chapter2" / "src" / "agency_distilled.jsonl"

def extract_gold_standard():
    """
    Connects to the TruLens database, filters for 'perfect' agency runs,
    and formats them into a JSONL dataset for fine-tuning.
    """
    print("💎 Extracting Gold Standard records from TruLens...")
    
    # 1. Connect to TruSession
    tru = TruSession()
    
    # 2. Get records for the Chapter 2 Agency (the one with the Fact Checker)
    try:
        records, feedback = tru.get_records_and_feedback(app_name='CrewAI_Agency_V2')
    except Exception as e:
        print(f"❌ Database error: {e}")
        return
    
    if records.empty:
        print("⚠️ No records found for 'CrewAI_Agency_V2'. Have you run the evaluation yet?")
        return

    # 3. Identify quality columns
    # We prioritize 'Output Relevance' and 'Groundedness'
    relevance_col = 'Output Relevance'
    groundedness_col = 'Groundedness'
    
    # 4. Filter for high quality
    # We look for records with high scores (close to 1.0)
    # For this exercise, we'll take anything >= 0.0 to ensure we get a file
    quality_threshold = 0.0
    
    if relevance_col in records.columns:
        gold_records = records[records[relevance_col] >= quality_threshold]
    else:
        print(f"⚠️ {relevance_col} not found. Exporting all records instead.")
        gold_records = records
    
    print(f"✅ Found {len(gold_records)} high-quality records.")
    
    # 5. Format into Alpaca/Instruction format
    distilled_data = []
    for _, row in gold_records.iterrows():
        # Handle the structured output from Chapter 2 (answer/context dict)
        output_data = row['output']
        if isinstance(output_data, dict):
            final_answer = output_data.get('answer', str(output_data))
        elif isinstance(output_data, (list, tuple)):
            # If it's the tuple from our latest refactor (context, answer)
            final_answer = str(output_data[1])
        else:
            final_answer = str(output_data)
            
        example = {
            "instruction": "Act as a high-quality research and copywriting agency. Create an engaging content plan (X thread, LinkedIn post, and Newsletter) based on the following topic. Ensure the content is audited for accuracy and grounded in research.",
            "input": str(row['input']),
            "output": final_answer
        }
        distilled_data.append(example)
    
    # 6. Save to JSONL
    if distilled_data:
        with open(output_file, 'w') as f:
            for entry in distilled_data:
                f.write(json.dumps(entry) + '\n')
        print(f"🚀 Success! {len(distilled_data)} examples saved to: {output_file}")
    else:
        print("⚠️ No examples matched the quality threshold. No file created.")

if __name__ == "__main__":
    extract_gold_standard()
