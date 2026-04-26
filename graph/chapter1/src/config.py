import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

class Config:
    # LLM Settings
    USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm(model_name=None):
    if Config.USE_OLLAMA:
        return ChatOllama(model=model_name or Config.OLLAMA_MODEL)
    else:
        return ChatOpenAI(model=model_name or Config.OPENAI_MODEL)

def get_search_tool(max_results=3):
    if not Config.TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not found. Search functionality will be disabled.")
        return None
    return TavilySearchResults(max_results=max_results)
