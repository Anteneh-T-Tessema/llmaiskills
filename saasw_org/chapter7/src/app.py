import os
import sys
import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Import our Gateway from Chapter 5
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from chapter5.gateway import SaaSwGateway

app = FastAPI(title="SaaSw Sovereign Dashboard")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REGISTRY_PATH = os.path.abspath("saasw_org/chapter5/config/registry.json")
gateway = SaaSwGateway(REGISTRY_PATH)

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    await gateway.connect_all()

@app.on_event("shutdown")
async def shutdown_event():
    await gateway.exit_stack.aclose()

@app.get("/")
async def get_index():
    return FileResponse("saasw_org/chapter7/static/index.html")

@app.get("/status")
async def get_status():
    tools = await gateway.list_global_tools()
    return {
        "nodes": list(gateway.sessions.keys()),
        "tools": list(tools.keys()),
        "status": "online"
    }

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize the Dashboard Brain
llm = ChatOllama(model="llama3.2")

@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        tools = await gateway.list_global_tools()
        tool_names = list(tools.keys())
        
        # 1. Ask the LLM which tools are needed
        router_prompt = (
            f"You are the Sovereign OS. You have access to these tools: {tool_names}. "
            f"The user says: '{request.query}'. "
            "If you need tools, respond ONLY with a comma-separated list of tool names. "
            "If you don't need tools, respond with your answer."
        )
        
        route_decision = llm.invoke([HumanMessage(content=router_prompt)]).content
        
        results = []
        # 2. Execute the chosen tools
        for t_name in tool_names:
            if t_name in route_decision:
                print(f"⚡️ Intelligent Route: Executing {t_name}...")
                # Simple argument mapping for the demo
                args = {"industry": "AI", "value": 100, "directory": "."}
                res = await gateway.call_node_tool(t_name, args)
                results.append(res.content[0].text)
        
        # 3. Summarize everything
        if results:
            summary_prompt = f"The user asked: {request.query}. The nodes returned: {results}. Summarize this into a professional dashboard report."
            final_answer = llm.invoke([HumanMessage(content=summary_prompt)]).content
            return {"answer": final_answer}
        else:
            return {"answer": route_decision}
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
