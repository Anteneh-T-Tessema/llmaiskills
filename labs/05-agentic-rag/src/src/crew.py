from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from tools.rag_tool import KnowledgeSearchTool

# Local LLM Configuration (Switching to Llama 3.2 for better Tool Compliance)
llm = LLM(
    model='ollama/llama3.2',
    base_url="http://localhost:11434",
    temperature=0
)

@CrewBase
class AgenticRAGCrew():
    """Agentic RAG Crew for Sovereign Content Operations"""

    @agent
    def strategic_researcher(self) -> Agent:
        return Agent(
            config={
                'role': 'Strategic Researcher',
                'goal': 'Gather intelligence on {topic} by first checking internal standards and then searching the web.',
                'backstory': (
                    "You are a compliant researcher. You MUST use the 'internal_knowledge_search' tool "
                    "to find the 'Groundedness Standards' before you do anything else. "
                    "NEVER provide a final answer until you have used the tool and received its output. "
                    "If you output JSON, you must do it ONLY to call a tool, never as a final answer."
                )
            },
            tools=[SerperDevTool(), KnowledgeSearchTool()],
            llm=llm,
            verbose=True,
            allow_delegation=False,
            max_iter=10
        )

    @agent
    def quality_editor(self) -> Agent:
        return Agent(
            config={
                'role': 'Quality Compliance Editor',
                'goal': 'Approve research based on the internal 0.9 threshold.',
                'backstory': (
                    "You are a strict compliance officer. You use 'internal_knowledge_search' "
                    "to verify standards. You never accept work that hasn't been cross-referenced."
                )
            },
            tools=[KnowledgeSearchTool()],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config={
                'description': (
                    "STRICT PROCESS:\n"
                    "1. Call 'internal_knowledge_search' with query='Groundedness Standards'.\n"
                    "2. Wait for the tool result.\n"
                    "3. Research {topic} on the web.\n"
                    "4. Write a report that incorporates the findings and states the compliance standard found in step 1."
                ),
                'expected_output': "A detailed research report. DO NOT output raw JSON in the final answer."
            },
            agent=self.strategic_researcher()
        )

    @task
    def compliance_task(self) -> Task:
        return Task(
            config={
                'description': (
                    "Use 'internal_knowledge_search' to find the 'Groundedness Standards' again. "
                    "Compare the researcher's report to this standard. Approve or reject."
                ),
                'expected_output': "A compliance decision memo."
            },
            agent=self.quality_editor()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
