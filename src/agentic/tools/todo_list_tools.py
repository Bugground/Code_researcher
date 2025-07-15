from typing import Annotated

from langchain.schema import HumanMessage
from langchain.schema.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from src.agentic.agents import State


@tool(parse_docstring=True)
def add_todo(
    title: str,
    state: Annotated[State, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """
    Add an item to the todo list. You should call this tool to update the plan before you start working on it.

    Args:
        title: The title of the todo to add. Use single line and plain text only.
        state:
        tool_call_id:
    """
    state.todo_list.add_todo(title)
    return Command(
        update={
            "todo_list": state.todo_list,
            "messages": [
                ToolMessage("Done", tool_call_id=tool_call_id),
                HumanMessage(content=state.todo_list.to_markdown(), id="todo_list"),
            ],
        }
    )


@tool(parse_docstring=True)
def mark_todo_as_done(
    id: int,
    state: Annotated[State, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """
    Mark a specific item as done in the todo list. You should call this tool to update the status once finished.

    Args:
        id: The id of the todo item to mark as done. The id is the number after the "#" in the todo list.
        state:
        tool_call_id:
    """
    state.todo_list.mark_todo_as_done(id)
    return Command(
        update={
            "todo_list": state.todo_list,
            "messages": [
                ToolMessage("Done", tool_call_id=tool_call_id),
                HumanMessage(content=state.todo_list.to_markdown(), id="todo_list"),
            ],
        }
    )
