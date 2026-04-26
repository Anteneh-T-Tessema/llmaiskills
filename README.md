# Sovereign AI Content Agency

A production-grade, multi-agent AI system designed for high-performance content research, generation, and auditing. This repository tracks the journey from prompt engineering to local fine-tuning on Apple Silicon.

## 🗂️ Repository Structure

```text
├── crewAI/             # Multi-agent orchestration (CrewAI)
│   ├── chapter1/       # Base 3-agent crew (Researcher, Copywriter, Editor)
│   └── chapter2/       # Resilient 4-agent crew (+ Accuracy Auditor)
├── graph/              # Graph-based workflows (LangGraph)
├── evals/              # TruLens v1.0 Evaluation suite
├── finetune/           # Fine-tuning & Distillation pipeline
│   ├── data/           # Gold Standard training datasets
│   ├── mlx/            # MLX Adapters for Apple Silicon
│   └── scripts/        # Distillation, Cleaning, and LoRA scripts
└── SOVEREIGN_AI_JOURNEY.md  # Master technical documentation
```

## 🚀 Quick Start

### 1. Run the Multi-Agent Agency
```bash
python crewAI/chapter2/src/main.py
```

### 2. Run Evaluations (TruLens)
```bash
python evals/chapter2/src/trulens_agency_v2.py
```

### 3. Local Fine-Tuning (M3 Max)
```bash
./finetune/run_mlx_training.sh
```

## 📖 The Journey
For a deep dive into the architecture, metrics, and fine-tuning results, see the [Sovereign AI Journey](SOVEREIGN_AI_JOURNEY.md).

---
**Maintained by**: Anteneh Tessema
**License**: MIT
