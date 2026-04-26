#!/bin/bash

# run_mlx_training.sh
# This script executes a local LoRA fine-tuning job on Apple Silicon.
# We use a small 1B model (Llama-3.2) for this practice run to ensure speed.

# 1. Configuration
MODEL="mlx-community/Llama-3.2-1B-Instruct-4bit"
DATA_DIR="/Users/antenehtessema/developer/graphcrewgen/evals/chapter2/src/mlx_data"
VENV_PYTHON="/Users/antenehtessema/developer/graphcrewgen/.venv/bin/python"

echo "🚀 Starting Local LoRA Training on M3 Max..."
echo "📦 Model: $MODEL"
echo "📂 Data: $DATA_DIR"

# 2. Run the MLX-LM LoRA training command
# --iters 100 is enough for a practice run to see the loss decrease
# --batch-size 1 is safe for all memory configurations
$VENV_PYTHON -m mlx_lm.lora \
    --model $MODEL \
    --train \
    --data $DATA_DIR \
    --iters 100 \
    --batch-size 1 \
    --learning-rate 2e-5 \
    --steps-per-report 10 \
    --steps-per-eval 50 \
    --adapter-path agency_mlx_adapter

echo "✅ Training session completed!"
echo "📂 Your adapters are saved in 'agency_mlx_adapter'"
echo "💡 You can now run the model using: mlx_lm.generate --model $MODEL --adapter-path agency_mlx_adapter"
