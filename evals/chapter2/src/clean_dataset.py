import json
import re
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
input_file = current_dir / "agency_distilled.jsonl"
output_file = current_dir / "agency_cleaned.jsonl"

def clean_data():
    """
    Scrub the distilled dataset to remove any tool-call hallucinations (JSON)
    or leftover agent meta-data. This ensures the final fine-tuning data
    is 'Gold Standard' quality.
    """
    if not input_file.exists():
        print(f"❌ Input file {input_file} not found. Run distill_dataset.py first.")
        return

    print("🧹 Cleaning dataset: Removing tool-call hallucinations...")
    
    cleaned_count = 0
    total_count = 0
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if not line.strip():
                continue
                
            total_count += 1
            data = json.loads(line)
            output = data['output']
            
            # 1. Regex to remove the "Here's the function call: { ... }" blocks
            # Adding \s*}? at the end to catch stray closing braces
            json_pattern = r"(Here's the function call:|I'll need to call the search_tool).*?\{.*?\"name\":\s*\"search_tool\".*?\}\s*}?"
            
            # 2. Regex to remove leftover Agent headers if the instrumentation captured them
            header_pattern = r"Agent:\s*\w+\s*Final Answer:\s*"
            
            new_output = output
            
            # Apply cleaning
            new_output = re.sub(json_pattern, "", new_output, flags=re.DOTALL)
            new_output = re.sub(header_pattern, "", new_output, flags=re.DOTALL)
            
            # 3. Final cleanup of leading/trailing noise
            new_output = new_output.strip()
            
            # Check if we actually changed anything
            if new_output != output:
                cleaned_count += 1
                
            data['output'] = new_output
            f_out.write(json.dumps(data) + '\n')
            
    print(f"📊 Summary:")
    print(f" - Total records: {total_count}")
    print(f" - Cleaned records: {cleaned_count}")
    print(f"🚀 Cleaned dataset saved to: {output_file}")

if __name__ == "__main__":
    clean_data()
