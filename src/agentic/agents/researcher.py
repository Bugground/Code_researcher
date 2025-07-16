from langgraph.prebuilt import create_react_agent

from src.agentic.agents.state import State
from src.agentic.tools import (
    file_outline,
    file_tree,
    react,
    read_lines,
    search_in_file,
    search_in_folders,
)
from src.llm.model import create_chat_model
from src.llm.prompt import apply_prompt_template


def create_researcher():
    chat_model = create_chat_model("pro")
    prompt = apply_prompt_template("researcher")
    tools = (
        file_outline,
        file_tree,
        read_lines,
        search_in_file,
        search_in_folders,
        react,
    )
    agent = create_react_agent(
        model=chat_model,
        tools=tools,
        prompt=prompt,
        state_schema=State,
        name="researcher",
    )
    return agent


researcher = create_researcher()
