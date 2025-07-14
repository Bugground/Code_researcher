from langgraph.prebuilt import create_react_agent

from agentic.notepad.notepad import create_notepad
from agentic.todo.todo_list import create_todo_list
from src.agentic.notepad import Notepad
from src.agentic.todo import TodoList
from src.agentic.tools import (
    create_notepad_tools,
    create_project_tools,
    create_todo_list_tools,
)
from src.llm.model import create_chat_model
from src.llm.prompt import apply_prompt_template
from src.workspace import Project


def create_researcher(project: Project, todo_list: TodoList, notepad: Notepad):
    chat_model = create_chat_model()
    tools = [
        *create_project_tools(project),
        *create_todo_list_tools(todo_list),
        *create_notepad_tools(notepad),
    ]
    prompt = apply_prompt_template("researcher")
    agent = create_react_agent(
        name="researcher",
        model=chat_model,
        tools=tools,
        prompt=prompt,
    )
    return agent


researcher = create_researcher(
    Project("/Users/henry/Desktop/code-play"), create_todo_list(), create_notepad()
)
