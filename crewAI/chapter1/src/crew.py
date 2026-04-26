from crewai import Crew, Process
from src.agents.researcher import create_researcher
from src.agents.copywriter import create_copywriter
from src.agents.seo_editor import create_seo_editor
from src.tasks.content_tasks import create_tasks

def run_agency(topic):
    # Initialize Agents
    researcher = create_researcher()
    copywriter = create_copywriter()
    editor = create_seo_editor()

    # Initialize Tasks
    tasks = create_tasks(researcher, copywriter, editor)

    # Define the Crew
    crew = Crew(
        agents=[researcher, copywriter, editor],
        tasks=tasks,
        process=Process.sequential, # Sequential workflow
        verbose=True
    )

    # Start the work
    # Note: kickoff returns a CrewOutput object in modern CrewAI
    result = crew.kickoff(inputs={'topic': topic})
    
    # In newer versions, result is a CrewOutput, we can get the raw string
    return str(result)
