import asyncio
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_ollama import ChatOllama
import json

# 1. Setup the Judge Brain
judge_llm = ChatOllama(model="llama3.2")

class OllamaJudge(DeepEvalBaseLLM):
    def __init__(self, model_name):
        self.model = ChatOllama(model=model_name)
    def load_model(self): return self.model
    def generate(self, prompt: str) -> str: return self.model.invoke(prompt).content
    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        return res.content
    def get_model_name(self): return "Llama 3.2"

async def run_master_eval(question, context, actual_output):
    print(f"\n🧪 MASTER EVALUATION GATE INITIATED")
    print(f"Target: {question[:50]}...")
    print("-" * 40)

    # --- LEVEL 1: SOVEREIGN JUDGE (Reasoning) ---
    print("⚖️ Level 1: Sovereign Reasoning Check...")
    prompt = f"Audit this. Context: {context}. Answer: {actual_output}. Return JSON {{'score': 0-1, 'reason': 'str'}}"
    sov_res = judge_llm.invoke(prompt).content
    # Simple extraction
    try:
        sov_data = json.loads(sov_res.strip().replace("```json", "").replace("```", ""))
        print(f"✅ Sovereign Score: {sov_data['score']} | Reason: {sov_data['reason'][:50]}...")
    except:
        print("⚠️ Sovereign Parsing Error (using fallback)")
        sov_data = {"score": 0.5}

    # --- LEVEL 2: DEEPEVAL (Deep Hallucination Check) ---
    print("🛡️ Level 2: DeepEval Hallucination Check...")
    ollama_model = OllamaJudge("llama3.2")
    metric = HallucinationMetric(threshold=0.5, model=ollama_model)
    test_case = LLMTestCase(input=question, actual_output=actual_output, context=[context])
    
    try:
        metric.measure(test_case)
        print(f"✅ DeepEval Score: {metric.score} | Success: {not metric.is_successful()}")
    except Exception as e:
        print(f"⚠️ DeepEval Error: {e}")

    # --- FINAL SCORE ---
    final_score = (sov_data['score'] + (1 - metric.score)) / 2
    print("-" * 40)
    print(f"🏆 FINAL QUALITY SCORE: {final_score:.2f}")
    
    if final_score < 0.7:
        print("❌ STATUS: QUALITY GATE REJECTED - RE-ROUTING AGENT")
    else:
        print("✨ STATUS: QUALITY GATE PASSED - DEPLOYING RESPONSE")

if __name__ == "__main__":
    # Test a Hallucination Case
    q = "What is our company's remote work policy?"
    c = "Policy: Remote work is allowed 3 days a week."
    a = "Policy: You can work from Hawaii forever and never come in."
    
    asyncio.run(run_master_eval(q, c, a))
