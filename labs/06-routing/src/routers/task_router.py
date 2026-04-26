import json
from typing import Literal, Dict
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

class RoutingDecision(BaseModel):
    model_choice: Literal["fast", "smart", "heavy"]
    reasoning: str

class TaskRouter:
    """
    Intelligent Router that selects the optimal LLM based on task complexity.
    - Fast: Llama-3.2-1B (Fine-tuned/Fast)
    - Smart: Llama-3.2-3B (Reliable tool calling)
    - Heavy: Llama-3-70B or similar (Complex reasoning)
    """
    def __init__(self):
        # The router itself should be lightweight
        self.router_llm = ChatOllama(model="llama3.2:1b", temperature=0)

    def get_route(self, task_description: str) -> Dict:
        system_prompt = (
            "You are an AI Resource Optimizer. Classify the task complexity.\n"
            "Categories:\n"
            "- 'fast': Content layout, formatting, or simple summaries.\n"
            "- 'smart': Research requiring tools, structured RAG, or logical steps.\n"
            "- 'heavy': Complex legal audits, architecture decisions, or deep creative writing.\n"
            "\n"
            "Response MUST be valid JSON with 'model_choice' and 'reasoning' keys."
        )
        
        try:
            response = self.router_llm.invoke(f"{system_prompt}\n\nTask: {task_description}")
            # Cleaning up the response to ensure valid JSON
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            decision = json.loads(content)
            return decision
        except Exception as e:
            print(f"⚠️ Router Error: {e}. Defaulting to 'smart' model.")
            return {"model_choice": "smart", "reasoning": "Fallback due to error."}

if __name__ == "__main__":
    router = TaskRouter()
    
    # Test 1: Simple task
    print("\n--- Testing Simple Task ---")
    print(router.get_route("Format this list of dates into ISO 8601 format."))
    
    # Test 2: Complex task
    print("\n--- Testing Complex Task ---")
    print(router.get_route("Analyze the legal implications of AI model weights being released under a custom open-source license."))
