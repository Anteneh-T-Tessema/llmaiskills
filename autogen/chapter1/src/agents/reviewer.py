from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

def create_reviewer():
    """
    Reviewer Agent: Executes code and provides feedback/errors.
    """
    # Initialize a local code executor
    executor = LocalCommandLineCodeExecutor(work_dir="workspace")
    
    return CodeExecutorAgent(
        name="Reviewer",
        code_executor=executor,
    )
