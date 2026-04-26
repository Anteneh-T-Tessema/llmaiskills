from crewai import Agent
from src.config import Config

def create_seo_editor():
    return Agent(
        role='SEO & Quality Editor',
        goal='Ensure all content is optimized for search and maintains a consistent, high-quality brand voice',
        backstory='You are the final gatekeeper. You check for clarity, SEO keywords, and ensure the content is ready for prime time.',
        llm=f"ollama/{Config.OLLAMA_MODEL}",
        verbose=True,
        allow_delegation=False
    )
