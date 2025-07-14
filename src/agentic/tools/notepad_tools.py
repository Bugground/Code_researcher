from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel

from src.agentic.notepad import Notepad


class AddNoteArgs(BaseModel):
    content: str
    """The content of the note to add. Use markdown format. At least contain one level-2 heading and content."""


def create_notepad_tools(notepad: Notepad) -> list[Tool]:
    results: list[Tool] = [
        StructuredTool.from_function(
            name="add_note",
            func=notepad.add_note,
            description="Add a markdown note to the notepad. Each note should contain at least one level-2 heading and content.",
            args_schema=AddNoteArgs,
        ),
    ]
    return results
