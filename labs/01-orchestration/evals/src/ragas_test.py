import os
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_similarity,
    answer_correctness
)
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI

# 1. Initialize local Evaluator
evaluator_llm = ChatOpenAI(
    model="llama3.1",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    temperature=0,
)

evaluator_embeddings = OllamaEmbeddings(model="llama3.2")

# 2. Prepare a Comprehensive Dataset (10 cases)
data_sample = {
    "question": [
        "What are the core requirements for Sovereign AI?",
        "How does the self-improvement loop work in Sovereign AI?",
        "What is the role of decentralized nodes?",
        "What is the purpose of autonomous auditing?",
        "How does Sovereign AI handle data privacy?",
        "What is the difference between Sovereign AI and traditional Cloud AI?",
        "Who owns the models in a Sovereign AI system?",
        "Can Sovereign AI operate offline?",
        "What are the security implications of autonomous agents?",
        "How is consensus reached in a decentralized AI network?"
    ],
    "answer": [
        "Sovereign AI requires decentralization, autonomous auditing, and self-improvement.",
        "It uses auditing feedback to refine decision parameters autonomously.",
        "Decentralized nodes provide censorship resistance and ensure no single entity controls the AI.",
        "Autonomous auditing ensures the AI's actions remain aligned with its core directives without external oversight.",
        "Data privacy is maintained through local execution and encrypted state synchronization across nodes.",
        "Sovereign AI operates locally or on decentralized infrastructure, unlike Cloud AI which depends on centralized servers.",
        "The models are owned by the users or the decentralized collective, not a single corporation.",
        "Yes, Sovereign AI is designed for local-first execution, allowing for offline operation with periodic sync.",
        "Security is enhanced by minimizing attack surfaces and using cryptographic verification for agent actions.",
        "Consensus is reached via cryptographic protocols that validate state transitions across the node network."
    ],
    "contexts": [
        ["Sovereign AI pillars: Decentralized nodes, autonomous auditing, and self-improvement loops."],
        ["The self-improvement loop utilizes feedback from autonomous auditing to refine the agent's decision-making parameters without human intervention."],
        ["Decentralized nodes ensure that no single entity has control over the AI's execution or data, providing resilience against censorship."],
        ["Autonomous auditing is a continuous process where internal monitors verify agent compliance with predefined safety and logic rules."],
        ["Privacy-first design involves local-only inference and the use of zero-knowledge proofs for cross-node state updates."],
        ["Traditional AI is hosted on central servers (Cloud AI), whereas Sovereign AI distributes compute across private or community-owned nodes."],
        ["Ownership is distributed; the model weights and training data are managed through decentralized governance protocols."],
        ["Local-first architecture ensures that the AI remains functional even when disconnected from the global network."],
        ["Security protocols for autonomous agents include sandboxed execution and hardware-level isolation to prevent unauthorized access."],
        ["Decentralized consensus mechanisms like Proof-of-Stake or Byzantine Fault Tolerance are adapted for AI state synchronization."]
    ],
    "ground_truth": [
        "Decentralization, autonomous auditing, and self-improvement.",
        "The loop uses feedback from autonomous auditing to improve decision-making parameters independently.",
        "They provide resilience against censorship and prevent centralized control.",
        "To ensure alignment with directives through continuous internal verification.",
        "Through local execution and secure, encrypted state management.",
        "Cloud AI is centralized; Sovereign AI is decentralized and local-first.",
        "Users or the decentralized community hold ownership via governance.",
        "Yes, it supports local execution and offline functionality.",
        "Improved security via reduced attack surfaces and cryptographic checks.",
        "Through decentralized protocols that verify and sync the AI's state."
    ]
}

dataset = Dataset.from_dict(data_sample)

def run_evaluation():
    print("🧪 Running Optimized Ragas Evaluation...")
    
    # 3. Execute with only ONE metric and ONE worker
    # This ensures the local LLM can focus
    try:
        result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
                answer_similarity,
                answer_correctness
            ],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
        )

        df = result.to_pandas()
        print("\n📊 EVALUATION REPORT")
        print("="*60)
        print(df)
    except Exception as e:
        print(f"❌ Eval failed: {e}")

if __name__ == "__main__":
    run_evaluation()
