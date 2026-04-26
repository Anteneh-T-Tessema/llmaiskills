import json
from pathlib import Path

# Setup paths
current_dir = Path(__file__).parent
input_file = current_dir / "agency_cleaned.jsonl"
mlx_data_dir = current_dir / "mlx_data"
mlx_data_dir.mkdir(exist_ok=True)

def prepare_mlx_dataset():
    """
    Converts the standard instruction dataset into the MLX-LM format.
    MLX-LM expects a simple JSONL with 'text' or 'prompt'/'completion' keys.
    """
    if not input_file.exists():
        print(f"❌ Input file {input_file} not found. Run clean_dataset.py first.")
        return

    print("🛠️ Formatting dataset for MLX-LM...")
    
    with open(input_file, 'r') as f:
        lines = [json.loads(line) for line in f if line.strip()]

    # MLX-LM training typically uses a single 'text' field 
    # that includes the full prompt and response.
    mlx_formatted = []
    for entry in lines:
        text = f"### Instruction:\n{entry['instruction']}\n\n### Input:\n{entry['input']}\n\n### Response:\n{entry['output']}<|endoftext|>"
        mlx_formatted.append({"text": text})

    # Since we only have a few examples for practice, 
    # we'll use the same data for train/valid/test just to demonstrate the loop.
    # In a real scenario, you'd split 80/10/10.
    
    for filename in ["train.jsonl", "valid.jsonl", "test.jsonl"]:
        with open(mlx_data_dir / filename, 'w') as f:
            for entry in mlx_formatted:
                f.write(json.dumps(entry) + '\n')

    print(f"✅ Created MLX dataset in: {mlx_data_dir}")
    print(f"📁 Files: train.jsonl, valid.jsonl, test.jsonl")

if __name__ == "__main__":
    prepare_mlx_dataset()
