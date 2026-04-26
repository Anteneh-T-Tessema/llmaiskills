import asyncio
import sys
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from src.agents.developer import create_developer
from src.agents.reviewer import create_reviewer

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Write a script to ...\"")
        return

    task = sys.argv[1]
    
    # Initialize Agents
    developer = create_developer()
    reviewer = create_reviewer()

    # Define Termination Condition
    termination = TextMentionTermination("TERMINATE")

    # Initialize Team
    team = RoundRobinGroupChat(
        [developer, reviewer],
        termination_condition=termination
    )

    print(f"🚀 Starting Dynamic Debugging Pair for: {task}")
    
    # Run the stream
    async for message in team.run_stream(task=task):
        if hasattr(message, 'source') and hasattr(message, 'content'):
            print(f"\n--- {message.source} ---\n{message.content}")
        elif hasattr(message, 'stop_reason'):
             print(f"\n--- Termination ---\nReason: {message.stop_reason}")
        else:
            print(f"\n--- System Event ---\n{message}")

if __name__ == "__main__":
    asyncio.run(main())
