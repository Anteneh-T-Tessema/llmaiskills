# The Sovereign AI Journey: From Prompting to Fine-Tuning

This document summarizes the engineering path we have taken to build a high-performance, local, and audited AI Content Agency.

---

## 🏛️ Chapter 1: The Multi-Agent Foundation
**Objective**: Orchestrate multiple specialized agents to perform a task better than a single model.
- **Technologies**: CrewAI, LangGraph, Ollama.
- **Key Achievements**:
    - Built a 3-agent Crew (Researcher, Copywriter, Editor).
    - Implemented a Graph-based research workflow for iterative summaries.
    - Integrated **TruLens v1.0** to measure "Output Relevance" using a local LLM evaluator.

## 🛡️ Chapter 2: The Resilient Agency
**Objective**: Eliminate hallucinations and ensure data-backed accuracy.
- **Key Achievements**:
    - Added the **Accuracy Auditor (Fact Checker)** agent.
    - Implemented the **Groundedness Metric**: Automatically cross-referencing final content against raw research notes.
    - Added **Safety Metrics**: Harmfulness and Maliciousness checks using TruLens.

## 🧪 Chapter 3: Distillation & Fine-Tuning
**Objective**: Compress multi-agent "intelligence" into a single, fast local model.
- **Key Achievements**:
    - **Dataset Extraction**: Built [distill_dataset.py](file:///Users/antenehtessema/developer/graphcrewgen/evals/chapter2/src/distill_dataset.py) to pull high-scoring runs from the database.
    - **Data Scrubbing**: Built [clean_dataset.py](file:///Users/antenehtessema/developer/graphcrewgen/evals/chapter2/src/clean_dataset.py) to remove tool-call hallucinations.
    - **Local LoRA Training**: Successfully fine-tuned a **Llama-3.2-1B** model on an **Apple M3 Max** using the **MLX** framework.
    - **Performance**: Achieved **135+ tokens/sec** with the specialized "Agency" behavior.

## 🚀 Chapter 4: The Sovereign Deployment
**Objective**: Move from experimental scripts to production-grade local tools.
- **Key Achievements**:
    - Provided [merge_and_export.py](file:///Users/antenehtessema/developer/graphcrewgen/evals/chapter2/src/merge_and_export.py) to bake adapters into base models.
    - Documented the **GGUF** conversion path for Ollama deployment.
    - **Comparison**: Proved that the fine-tuned model outperforms the base model in structure, tone, and efficiency.

---

## 🗺️ Next Steps: The Road Ahead

### 🛰️ Chapter 5: Agentic RAG & Memory
**Goal**: Give the agency a "Brain" (Long-term memory) and "Eyes" (Vector Search).
- Implement a Vector Database (ChromaDB or Qdrant).
- Create "Agentic RAG" where the Researcher decides when and where to search based on previous tasks.

### 🧩 Chapter 6: Multi-Model Orchestration & Routing
**Goal**: Optimize for cost and quality by choosing the right model for the right task.
- Build a "Router" agent that sends simple tasks to your 1B Fine-tuned model and complex tasks to Llama-3-70B.
- Implement "Prompt Caching" to handle massive research contexts efficiently.

### 🤖 Chapter 7: Autonomous Self-Improvement
**Goal**: A system that trains itself.
- Build a loop where TruLens automatically triggers a fine-tuning job whenever it collects 100 "Gold Standard" examples.
- Implement "RLHF at Home" (Reinforcement Learning from Human Feedback).

---

## 🛠️ Essential Commands
- **Run Agency**: `python crewAI/chapter1/src/main.py`
- **Evaluate**: `python evals/chapter2/src/trulens_agency_v2.py`
- **Distill Data**: `python evals/chapter2/src/distill_dataset.py`
- **Train Local LoRA**: `./evals/chapter2/src/run_mlx_training.sh`
- **Test Model**: `python -m mlx_lm.generate --model <base> --adapter-path agency_mlx_adapter`
