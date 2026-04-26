import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_ollama import ChatOllama

# 1. Custom LLM Wrapper for DeepEval (using Ollama)
class OllamaLlama3(DeepEvalBaseLLM):
    def __init__(self, model_name):
        self.model = ChatOllama(model=model_name)

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Llama 3.2 (Ollama)"

# 2. Define the Test
def test_sovereign_hallucination():
    # The Model under test
    ollama_model = OllamaLlama3("llama3.2")
    
    # The Metric
    metric = HallucinationMetric(threshold=0.5, model=ollama_model)
    
    # The Test Case
    test_case = LLMTestCase(
        input="Describe Sovereign AI scaling.",
        actual_output="Sovereign AI scales by using massive cloud data centers managed by Big Tech.",
        context=["Sovereign AI scales through decentralized nodes and peer-to-peer verification, avoiding central cloud clusters."]
    )
    
    # Assert
    assert_test(test_case, [metric])

if __name__ == "__main__":
    # In DeepEval, you usually run with 'deepeval test run'
    # But for this demo, we use a manual trigger
    print("🛡️ Running DeepEval Hallucination Test...")
    test_sovereign_hallucination()
