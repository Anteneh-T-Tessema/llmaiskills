import time
from routers.task_router import TaskRouter

def run_orchestrator():
    router = TaskRouter()
    
    tasks = [
        "Create a simple X thread layout for the topic 'Benefits of walking'.",
        "Perform a deep research into the molecular structure of new sustainable bioplastics.",
        "Audit this 5000-word research report for factual contradictions and safety compliance."
    ]
    
    print("🚦 Starting Multi-Model Orchestrator...")
    print("==========================================")
    
    for i, task in enumerate(tasks, 1):
        print(f"\n📝 Task {i}: {task}")
        
        start_time = time.time()
        decision = router.get_route(task)
        route_time = time.time() - start_time
        
        model = decision.get("model_choice")
        reasoning = decision.get("reasoning")
        
        print(f"🎯 Route: {model.upper()}")
        print(f"💡 Reason: {reasoning}")
        print(f"⏱️ Decision Time: {route_time:.2f}s")
        
        # In a real system, we would now dispatch to the specific model:
        # if model == "fast": use_fine_tuned_1b(task)
        # elif model == "smart": use_llama_3_2_3b(task)
        # ...

if __name__ == "__main__":
    run_orchestrator()
