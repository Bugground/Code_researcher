import os

from src.core.fs.ignore_rules import IgnoreRule


def file_tree(path: str, ignore_rules: list[IgnoreRule] = None) -> str:
    def generate_tree(path: str, prefix: str = ""):
        tree = []
        items = sorted(os.listdir(path))

        for index, item in enumerate(items):
            full_path = os.path.join(path, item)

            if ignore_rules and any(rule(full_path) for rule in ignore_rules):
                continue

            is_last = index == len(items) - 1
            connector = "└── " if is_last else "├── "
            tree.append(
                f"{prefix}{connector}{item}{'/' if os.path.isdir(full_path) else ''}"
            )

            if os.path.isdir(full_path):
                extension = "    " if is_last else "│   "
                tree.extend(generate_tree(full_path, prefix + extension))
        return tree

    root_name = os.path.basename(os.path.abspath(path))
    tree = [f"{root_name}/"] + generate_tree(
        path,
    )
    return "\n".join(tree)
