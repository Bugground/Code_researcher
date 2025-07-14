from langgraph.prebuilt import create_react_agent

from src.agentic.agents.state import State
from src.agentic.tools import add_note, add_todo, mark_todo_as_done, remove_todo
from src.llm.model import create_chat_model
from src.llm.prompt import apply_prompt_template


def create_researcher():
    chat_model = create_chat_model()
    tools = [add_note, add_todo, mark_todo_as_done, remove_todo]
    prompt = apply_prompt_template("researcher")
    agent = create_react_agent(
        name="researcher",
        model=chat_model,
        tools=tools,
        prompt=prompt,
        state_schema=State,
    )
    return agent


researcher = create_researcher()
