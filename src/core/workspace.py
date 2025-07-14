import os

from src.core.code import code_outline
from src.core.fs import (
    IgnoreRule,
    file_tree,
    ignore_rules_from_gitignore_files,
    read_file,
)
from src.core.search import search_in_file, search_in_folders


class Workspace:
    ignore_rules: list[IgnoreRule]

    def __init__(self, work_dir: str):
        self.work_dir = work_dir
        self.ignore_rules = [ignore_rules_from_gitignore_files(work_dir)]

    def map_path(self, path: str) -> str:
        return os.path.join(self.work_dir, path)

    def rel_path(self, path: str) -> str:
        if path.startswith(self.work_dir):
            return path.replace(self.work_dir, ".")
        return path

    def read_file(self, path: str, line_range: tuple[int, int] | None = None) -> str:
        return read_file(self.map_path(path), line_range)

    def file_tree(self) -> str:
        return file_tree(self.work_dir, ignore_rules=self.ignore_rules)

    def file_outline(self, path: str) -> str:
        if path.endswith(".py"):
            return code_outline(self.map_path(path))
        else:
            raise ValueError(f"Unsupported code file extension: {path}")

    def search_in_folders(
        self,
        keyword: str,
        folders: list[str],
        file_extensions: list[str],
    ) -> str:
        results = search_in_folders(
            keyword,
            [self.map_path(folder) for folder in folders],
            file_extensions,
            self.ignore_rules,
        )
        if len(results) == 0:
            return "No search result found"
        result_str = ""
        for result in results:
            for line in result.lines:
                result_str += f'File "{self.rel_path(result.file_path)}", line {line.line_number}: {line.context}\n'
            result_str += "\n"
        return result_str

    def search_in_file(self, keyword: str, file: str) -> str:
        result = search_in_file(keyword, self.map_path(file))
        if result is None:
            return "No search result found"
        result_str = ""
        for line in result.lines:
            result_str += f"Line {line.line_number}: {line.context}\n"
        return result_str


if __name__ == "__main__":
    workspace = Workspace("/Users/henry/Desktop/code-play")
    search_result = workspace.search_in_folders(
        "search",
        ["src"],
        ["py"],
    )
    print(search_result)
