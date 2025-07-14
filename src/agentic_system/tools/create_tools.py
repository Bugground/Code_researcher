from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel

from src.core.project import Project


class ZeroArgs(BaseModel):
    pass


class FileOutlineArgs(BaseModel):
    path: str
    """
    The path to **Python** the code file to get the outline of.
    Only Python files are supported.
    """


class ReadFileArgs(BaseModel):
    path: str
    """
    The path to the file to read.
    """

    from_line: int | None = None
    """
    The line range to read. Start and end are inclusive. `1` means the first line.
    If `from_line` is provided, `to_line` is required.
    """

    to_line: int | None = None
    """
    The line range to read. Start and end are inclusive. `1` means the first line.
    If both are `None`, read the whole file.
    If `to_line` is provided, `from_line` is required.
    """


class SearchInFoldersArgs(BaseModel):
    keyword: str
    """
    The keyword to search for. Case-insensitive.
    "abc bcd" means to search for lines exactly contains "abc bcd".
    """

    folders: list[str]
    """
    The folders to search in.
    """

    file_extensions: list[str]
    """
    The file extensions to search in. e.g. `["py", "md", "ts". "tsx"]`.
    Wildcard like `*` is not supported.
    """


class SearchInFileArgs(BaseModel):
    keyword: str
    """
    The keyword to search for. Case-insensitive.
    "abc bcd" means search for files exactly contains "abc bcd".
    """
    file: str
    """
    The path to the file to search in.
    """


def create_tools_for_project(project: Project) -> list[Tool]:
    results: list[Tool] = [
        StructuredTool.from_function(
            name="file_tree",
            func=project.file_tree,
            description="Get the file tree of the current repository.",
            args_schema=ZeroArgs,
        ),
        StructuredTool.from_function(
            name="file_outline",
            func=project.file_outline,
            description="Get the outline of a code file.",
            args_schema=FileOutlineArgs,
        ),
        StructuredTool.from_function(
            name="search_in_folders",
            func=project.search_in_folders,
            description="Search keyword in specific folders.",
            args_schema=SearchInFoldersArgs,
        ),
        StructuredTool.from_function(
            name="search_in_file",
            func=project.search_in_file,
            description="Search keyword in a specific file.",
            args_schema=SearchInFileArgs,
        ),
        StructuredTool.from_function(
            name="read_file",
            func=project.read_file,
            description="Read a file. To save token usage, leverage the 'from_line' and 'to_line' params to specify a range.",
            args_schema=ReadFileArgs,
        ),
    ]
    return results
