"""
Merge and Export: Baking the Intelligence into the Model
Once fine-tuning is done, you have a "Base Model" and a small "Adapter".
To deploy this as a standalone model (for Ollama or GGUF), 
you must merge the adapter weights back into the base model.

Prerequisites:
    pip install torch transformers peft
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 1. Configuration
model_id = "meta-llama/Meta-Llama-3-8B-Instruct" # The original base model
adapter_dir = "./agency_lora_adapter"           # Where your training script saved the LoRA
output_dir = "./agency_model_merged"            # Final standalone model path

def merge_lora_to_base():
    print(f"📥 Loading base model: {model_id}")
    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # 2. Load the Adapter
    print(f"🔗 Attaching LoRA adapter from {adapter_dir}...")
    model = PeftModel.from_pretrained(base_model, adapter_dir)
    
    # 3. Merge Weights
    # This "bakes" the LoRA weights into the base model's matrices
    print("🔥 Merging weights (this may take a few minutes)...")
    merged_model = model.merge_and_unload()
    
    # 4. Save the Final Model
    print(f"💾 Saving standalone model to {output_dir}...")
    merged_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"✅ Success! Your Sovereign Agency model is ready at {output_dir}")

if __name__ == "__main__":
    # Note: This requires the base model and adapter to exist in the specified paths
    # merge_lora_to_base()
    pass

"""
NEXT STEPS: Converting to GGUF for Ollama

Once you have the merged model, you use llama.cpp to convert it:

1. Clone llama.cpp: 
   git clone https://github.com/ggerganov/llama.cpp

2. Install requirements:
   pip install -r llama.cpp/requirements.txt

3. Convert to GGUF:
   python llama.cpp/convert.py agency_model_merged --outfile agency_model.gguf --outtype q4_k_m

4. Create Ollama Model:
   Create a file named 'Modelfile':
   ---
   FROM ./agency_model.gguf
   TEMPLATE \"{{ .System }}\nUSER: {{ .Prompt }}\nASSISTANT: \"
   ---
   
   Run:
   ollama create agency-v2 -f Modelfile
"""
