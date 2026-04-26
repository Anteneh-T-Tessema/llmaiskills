import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

def get_model_client():
    """
    Returns a modern AutoGen model client configured for Ollama.
    """
    return OpenAIChatCompletionClient(
        model=os.getenv("OLLAMA_MODEL", "llama3.1"),
        base_url="http://localhost:11434/v1",
        api_key="ollama", # Placeholder for Ollama
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "llama3",
        }
    )
