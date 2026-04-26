from crewai import Crew, Task, Process
from src.agents.auditor import create_auditor_agent

def run_bridge_demo():
    # 1. Initialize the Agent
    auditor = create_auditor_agent()

    # 2. Define the Audit Task
    audit_task = Task(
        description=(
            "Audit the following scenario: A project started with 100,000 USD and "
            "ended with 145,000 USD. "
            "Step 1: Calculate the ROI using the tool.\n"
            "Step 2: Convert the final amount (145,000 USD) into GBP.\n"
            "Step 3: Provide a 2-sentence summary of the financial health.\n"
            "FINAL RULE: Once you have these numbers, STOP and provide your final answer immediately."
        ),
        expected_output="A financial audit report with ROI and converted currency values.",
        agent=auditor
    )

    # 3. Form the Crew
    crew = Crew(
        agents=[auditor],
        tasks=[audit_task],
        process=Process.sequential
    )

    print("🌉 Starting the Agentic Bridge (CrewAI + MCP)...")
    result = crew.kickoff()
    print("\n\n" + "="*30)
    print("FINAL AUDIT REPORT")
    print("="*30)
    print(result)

if __name__ == "__main__":
    run_bridge_demo()
