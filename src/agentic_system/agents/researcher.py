from langgraph.prebuilt import create_react_agent

from src.agentic_system.models import create_chat_model
from src.agentic_system.tools import create_tools_for_project
from src.core.project import Project


def create_researcher(project: Project):
    chat_model = create_chat_model()
    agent = create_react_agent(
        name="researcher",
        model=chat_model,
        tools=create_tools_for_project(project),
        prompt="You are a research agent. You are given a project and you need to research the project and answer the question using the tools provided.",
    )
    return agent


researcher = create_researcher(Project("/Users/henry/Desktop/code-play"))
