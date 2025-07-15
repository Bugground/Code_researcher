from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.agentic.agents import State


@tool(parse_docstring=True)
def file_tree(state: Annotated[State, InjectedState]) -> str:
    """
    Get the file tree of the current repository.

    Args:
        state:
    """
    return state.project.file_tree()


@tool(parse_docstring=True)
def file_outline(path: str, state: Annotated[State, InjectedState]) -> str:
    """
    Get the outline of a Python file, as well as line range of each member.
    Use this tool together with `read_lines` to get the code of a specific member.
    **Only Python files are supported**

    Args:
        path: The path to a Python code file. e.g. "./src/file.py"
        state:
    """
    return state.project.file_outline(path)


@tool(parse_docstring=True)
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
        state:
    """
    return state.project.search_in_folders(keyword, folders, file_extensions)


@tool(parse_docstring=True)
def search_in_file(
    keyword: str, file: str, state: Annotated[State, InjectedState]
) -> str:
    """
    Search keyword in a specific file.

    Args:
        keyword: The keyword to search for. e.g. "abc def" means search for exact match of "abc def"
        file: The path to the code file. e.g. "./src/file.py"
        state:
    """
    return state.project.search_in_file(keyword, file)


@tool(parse_docstring=True)
def read_lines(
    path: str,
    from_line: int | None,
    to_line: int | None,
    state: Annotated[State, InjectedState],
) -> str:
    """
    Read lines from a text file. To save token usage, leverage the 'from_line' and 'to_line' params to specify a range.

    Args:
        path: The path to the code file. e.g. "./src/file.py"
        from_line: The line number to start reading from. e.g. 10
        to_line: The line number to stop reading at. e.g. 20
    """
    from_line = from_line or 1
    to_line = to_line or 50
    full_lines = state.project.read_lines(path)
    hint = ""
    if len(full_lines) > from_line - to_line + 1:
        hint = (
            f"\n\n---\n\nThe content has been truncated. The actual file has {len(full_lines)} lines in total."
            + "\n- Use `add_note` to note your findings **immediately**"
            + "\n- Then use `read_lines(path, from, to)` to read the rest if needed"
            + (
                "\n- Use `file_outline` to get the outline of the file, as well as line range of each member."
                if path.endswith(".py")
                else ""
            )
        )
    return "".join(full_lines[from_line - 1 : to_line]) + hint
