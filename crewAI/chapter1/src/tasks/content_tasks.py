from crewai import Task

def create_tasks(researcher, copywriter, editor):
    research_task = Task(
        description=(
            "Research the topic: {topic}. "
            "Identify 3 key insights and 1 unique angle that would make for viral content."
        ),
        expected_output="A detailed research report with key insights and a unique angle.",
        agent=researcher
    )

    copywriting_task = Task(
        description=(
            "Using the research provided, create a content plan that includes: "
            "1. An X thread (5-7 tweets) "
            "2. A LinkedIn post "
            "3. A Newsletter summary "
            "The content must be engaging and tailored to each platform's audience."
        ),
        expected_output="A multi-platform content plan including an X thread, LinkedIn post, and Newsletter summary.",
        agent=copywriter
    )

    editing_task = Task(
        description=(
            "Review the content plan for SEO optimization, clarity, and brand consistency. "
            "Ensure the tone is professional yet engaging."
        ),
        expected_output="The final, polished content plan ready for publication.",
        agent=editor
    )

    return [research_task, copywriting_task, editing_task]
