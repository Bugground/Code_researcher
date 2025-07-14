from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel

from src.agentic.todo import TodoList


class AddTodoArgs(BaseModel):
    content: str
    """The content of the TODO to add. Use single line and plain text only."""


class MarkTodoAsDoneArgs(BaseModel):
    id: int
    """The id of the TODO item to mark as done. The id is the number after the "#" in the todo list."""


class RemoveTodoArgs(BaseModel):
    id: int
    """The id of the TODO item to remove. The id is the number after the "#" in the todo list."""


def create_todo_list_tools(todo_list: TodoList) -> list[Tool]:
    results: list[Tool] = [
        StructuredTool.from_function(
            name="add_todo",
            func=todo_list.add_todo,
            description="Add an item to the TODO list. You should call this tool to update the plan before you start working on it.",
            args_schema=AddTodoArgs,
        ),
        StructuredTool.from_function(
            name="remove_todo",
            func=todo_list.remove_todo,
            description="Remove a specific item from the TODO list when the TODO item is not needed anymore or failed.",
            args_schema=RemoveTodoArgs,
        ),
        StructuredTool.from_function(
            name="mark_todo_as_done",
            func=todo_list.mark_todo_as_done,
            description="Mark a specific item as done in the TODO list. You should call this tool to update the status once finished.",
            args_schema=MarkTodoAsDoneArgs,
        ),
    ]
    return results
