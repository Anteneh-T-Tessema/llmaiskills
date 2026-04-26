import os
import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# 1. Initialize the Judge
judge = ChatOllama(model="llama3.2")

def evaluate_faithfulness(question, context, answer):
    print(f"🧪 Judging Faithfulness for: {question[:30]}...")
    
    prompt = f"""
    You are an expert Auditor. Compare the ANSWER to the CONTEXT provided.
    Determine if the ANSWER is faithful to the CONTEXT (no hallucinations).
    
    CONTEXT: {context}
    ANSWER: {answer}
    
    Respond ONLY with a JSON object in this format:
    {{
        "score": 0.0 to 1.0,
        "reason": "Brief explanation of why"
    }}
    """
    
    try:
        response = judge.invoke([HumanMessage(content=prompt)])
        # Clean the response in case the LLM adds markdown backticks
        clean_json = response.content.strip().replace("```json", "").replace("```", "")
        result = json.loads(clean_json)
        return result
    except Exception as e:
        return {"score": 0, "reason": f"Parsing Error: {str(e)}"}

if __name__ == "__main__":
    # Test Data
    q = "What are the core requirements for Sovereign AI?"
    c = "Pillars: Decentralization, Auditing, Self-improvement."
    a = "It needs decentralization and auditing."
    
    report = evaluate_faithfulness(q, c, a)
    
    print("\n📊 SOVEREIGN EVALUATION REPORT")
    print("="*40)
    print(f"FAITHFULNESS SCORE: {report['score']}")
    print(f"REASONING: {report['reason']}")
