"""
Fine-Tuning Template: Distilling the Agency into a Single Model
This script demonstrates how to perform QLoRA (4-bit LoRA) fine-tuning
using the HuggingFace ecosystem (trl, peft, transformers).

Prerequisites:
    pip install torch transformers peft trl accelerate bitsandbytes
"""

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# 1. Configuration
model_id = "meta-llama/Meta-Llama-3-8B-Instruct" # Base model to be "taught"
dataset_path = "agency_cleaned.jsonl"
output_dir = "./agency_lora_adapter"

# 2. BitsAndBytes Config (QLoRA)
# This compresses the base model into 4-bit to save VRAM
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# 3. Load Model and Tokenizer
print(f"📥 Loading base model: {model_id}")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# 4. Prepare for PEFT (LoRA)
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,             # Rank: Higher = more parameters to train
    lora_alpha=32,    # Scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"], # Target attention layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 5. Load and Format Dataset
def format_instruction(sample):
    return f"""### Instruction:
{sample['instruction']}

### Input:
{sample['input']}

### Response:
{sample['output']}"""

dataset = load_dataset("json", data_files=dataset_path, split="train")

# 6. Training Arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    max_steps=100, # Set epochs=3 for a real run
    optim="paged_adamw_8bit",
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    report_to="none" # Connect to WandB here
)

# 7. Initialize Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    max_seq_length=2048,
    tokenizer=tokenizer,
    args=training_args,
    formatting_func=format_instruction,
)

# 8. Start Training
print("🚀 Starting Fine-Tuning...")
# trainer.train() 

# 9. Save the Adapter
# trainer.save_model(output_dir)
print(f"✅ Training complete! Adapters saved to {output_dir}")

"""
Final Step: Inference with the Adapter
To use the new model, you load the base model and then attach the adapter:

from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained(model_id)
ft_model = PeftModel.from_pretrained(base_model, output_dir)
"""
