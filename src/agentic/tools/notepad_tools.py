from typing import Annotated

from langchain.schema import HumanMessage
from langchain.schema.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from src.agentic.agents import State


@tool
def add_note(
    content: str,
    state: Annotated[State, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
):
    """
    Add a markdown note to the notepad. Each note should contain at least one level-2 heading and content.

    Args:
        content: The markdown content of the note to add.
    """
    state.notepad.add_note(content)
    return Command(
        update={
            "notepad": state.notepad,
            "messages": [
                ToolMessage("Done", tool_call_id=tool_call_id),
                HumanMessage(content=state.notepad.to_markdown(), id="notepad"),
            ],
        }
    )
