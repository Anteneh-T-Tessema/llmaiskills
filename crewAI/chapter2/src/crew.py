from crewai import Crew, Process
from src.agents.researcher import create_researcher
from src.agents.copywriter import create_copywriter
from src.agents.fact_checker import create_fact_checker
from src.agents.seo_editor import create_seo_editor
from src.tasks.content_tasks import create_tasks

def run_agency(topic):
    # Initialize Agents
    researcher = create_researcher()
    copywriter = create_copywriter()
    fact_checker = create_fact_checker()
    editor = create_seo_editor()

    # Initialize Tasks
    tasks = create_tasks(researcher, copywriter, fact_checker, editor)

    # Define the Crew
    crew = Crew(
        agents=[researcher, copywriter, fact_checker, editor],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    # Start the work
    result = crew.kickoff(inputs={'topic': topic})
    
    # Return both the final output and the research context for Groundedness evaluation
    return {
        "answer": str(result.raw),
        "context": str(result.tasks_output[0].raw)
    }
