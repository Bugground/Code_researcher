from typing import Annotated

from langchain.schema import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel

from src.agentic.notepad import Notepad
from src.agentic.todo import TodoList
from src.workspace.project import Project


class State(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    remaining_steps: int = 25

    # project: Project
    todo_list: TodoList
    notepad: Notepad


def create_initial_state(
    project: Project,
) -> State:
    notepad = Notepad(notes=[])
    notepad.add_note(f"## File Tree\n\n```\n{project.file_tree()}\n```")
    todo_list = TodoList(items=[])
    todo_list.add_todo("Get file tree of the project")
    todo_list.mark_todo_as_done(1)
    return State(
        messages=[],
        todo_list=todo_list,
        notepad=notepad,
        remaining_steps=200,
    )
