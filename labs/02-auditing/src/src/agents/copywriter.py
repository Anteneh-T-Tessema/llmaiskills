from crewai import Agent
from src.config import Config

def create_copywriter():
    return Agent(
        role='Viral Copywriter',
        goal='Transform research into high-engagement content for X, LinkedIn, and Newsletters',
        backstory='You know exactly how to write for different platforms. You craft punchy X threads, professional LinkedIn posts, and concise Newsletter summaries.',
        llm=f"ollama/{Config.OLLAMA_MODEL}",
        verbose=True,
        allow_delegation=False
    )
