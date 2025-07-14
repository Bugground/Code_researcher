import ast


def outline_of_python_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            file_content = file.read()

        tree = ast.parse(file_content)

        outline = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_range = (
                    f"[{node.lineno}, {node.end_lineno}]"
                    if hasattr(node, "end_lineno")
                    else f"[{node.lineno}, ?]"
                )
                outline.append(f"Class: {node.name}, line_range={class_range}")
                for class_member in node.body:
                    if isinstance(class_member, ast.FunctionDef):
                        method_range = (
                            f"[{class_member.lineno}, {class_member.end_lineno}]"
                            if hasattr(class_member, "end_lineno")
                            else f"[{class_member.lineno}, ?]"
                        )
                        outline.append(
                            f"  Method: {class_member.name}, line_range={method_range}"
                        )
                    elif isinstance(class_member, ast.Assign):
                        for target in class_member.targets:
                            if isinstance(target, ast.Name):
                                attr_range = (
                                    f"[{class_member.lineno}, {class_member.end_lineno}]"
                                    if hasattr(class_member, "end_lineno")
                                    else f"[{class_member.lineno}, ?]"
                                )
                                outline.append(
                                    f"  Attribute: {target.id}, line_range={attr_range}"
                                )
            elif isinstance(node, ast.FunctionDef):
                func_range = (
                    f"[{node.lineno}, {node.end_lineno}]"
                    if hasattr(node, "end_lineno")
                    else f"[{node.lineno}, ?]"
                )
                outline.append(f"Function: {node.name}, line_range={func_range}")
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_range = (
                            f"[{node.lineno}, {node.end_lineno}]"
                            if hasattr(node, "end_lineno")
                            else f"[{node.lineno}, ?]"
                        )
                        outline.append(f"Variable: {target.id}, line_range={var_range}")

        return "\n".join(outline)

    except FileNotFoundError:
        return f"Error: File not found at path '{path}'"
    except Exception as e:
        return f"Error: {str(e)}"


# 示例用法
if __name__ == "__main__":
    path_to_file = "/Users/henry/Desktop/code-play/src/core/workspace.py"  # 替换为你的 .py 文件路径
    print(outline_of_python_file(path_to_file))
