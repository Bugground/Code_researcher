from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.agentic.agents import State


@tool
def file_tree(state: Annotated[State, InjectedState]) -> str:
    """
    Get the file tree of the current repository.
    """
    return state.project.file_tree()


@tool
def file_outline(path: str, state: Annotated[State, InjectedState]) -> str:
    """
    Get the outline of a code file. Only Python files are supported.

    Args:
        path: The path to the code file. e.g. "./src/file.py"
    """
    return state.project.file_outline(path)


@tool
def search_in_folders(
    keyword: str,
    folders: list[str],
    file_extensions: list[str],
    state: Annotated[State, InjectedState],
) -> str:
    """
    Search keyword in specific folders.

    Args:
        keyword: The keyword to search for. e.g. "abc def" means search for exact match of "abc def"
        folders: The folders to search in. e.g. ["./src", "./tests"]
        file_extensions: The file extensions to search in. e.g. ["py", "md"]
    """
    return state.project.search_in_folders(keyword, folders, file_extensions)


@tool
def search_in_file(
    keyword: str, file: str, state: Annotated[State, InjectedState]
) -> str:
    """
    Search keyword in a specific file.

    Args:
        keyword: The keyword to search for. e.g. "abc def" means search for exact match of "abc def"
        file: The path to the code file. e.g. "./src/file.py"
    """
    return state.project.search_in_file(keyword, file)


@tool
def read_file(
    path: str,
    from_line: int | None,
    to_line: int | None,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Read a file. To save token usage, leverage the 'from_line' and 'to_line' params to specify a range.

    Args:
        path: The path to the code file. e.g. "./src/file.py"
        from_line: The line number to start reading from. e.g. 10
        to_line: The line number to stop reading at. e.g. 20
    """
    return state.project.read_file(path, from_line, to_line)
