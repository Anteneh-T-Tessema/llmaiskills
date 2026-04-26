import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

class Config:
    # LLM Settings
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    @staticmethod
    def get_llm():
        return ChatOllama(model=Config.OLLAMA_MODEL)
