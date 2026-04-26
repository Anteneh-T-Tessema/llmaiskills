from crewai import Agent
from src.config import Config

def create_fact_checker():
    return Agent(
        role='Accuracy Auditor',
        goal='Cross-reference the Copywriter\'s content with the Researcher\'s raw findings to ensure 100% groundedness.',
        backstory="""You are a meticulous auditor. Your job is to ensure that no claims are made in the final 
        content that weren't supported by the initial research. You highlight hallucinations and ensure 
        the final output is perfectly grounded in the provided context.""",
        llm=f"ollama/{Config.OLLAMA_MODEL}",
        verbose=True,
        allow_delegation=False
    )
