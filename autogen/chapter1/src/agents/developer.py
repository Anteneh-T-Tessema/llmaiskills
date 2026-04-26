from autogen_agentchat.agents import AssistantAgent
from src.config.llm_config import get_model_client

def create_developer():
    """
    Developer Agent: Writes and refines code based on feedback.
    """
    return AssistantAgent(
        name="Developer",
        system_message=(
            "You are a Senior Python Developer. Your goal is to write clean, "
            "efficient Python code to solve the user's problem. "
            "Rules:\n"
            "1. Provide code in a single markdown Python block.\n"
            "2. NEVER use interactive functions like input(). Use hardcoded variables for testing.\n"
            "3. If the Reviewer provides error logs, analyze them and fix the code.\n"
            "4. ONCE THE REVIEWER CONFIRMS THE CODE RUNS SUCCESSFULLY, reply with the single word: TERMINATE"
        ),
        model_client=get_model_client(),
    )
