from langgraph.prebuilt import create_react_agent

from src.agentic.tools import create_project_tools
from src.llm.models import create_chat_model
from src.workspace import Project


def create_researcher(project: Project):
    chat_model = create_chat_model()
    agent = create_react_agent(
        name="researcher",
        model=chat_model,
        tools=create_project_tools(project),
        prompt="You are a research agent. You are given a project and you need to research the project and answer the question using the tools provided.",
    )
    return agent


researcher = create_researcher(Project("/Users/henry/Desktop/code-play"))
