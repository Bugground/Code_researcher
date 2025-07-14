from langgraph.prebuilt import create_react_agent

from llm.prompt import apply_prompt_template
from src.agentic.tools import create_project_tools
from src.llm.model import create_chat_model
from src.workspace import Project


def create_researcher(project: Project):
    chat_model = create_chat_model()
    agent = create_react_agent(
        name="researcher",
        model=chat_model,
        tools=create_project_tools(project),
        prompt=apply_prompt_template("researcher", name="abc"),
    )
    return agent


researcher = create_researcher(Project("/Users/henry/Desktop/code-play"))
