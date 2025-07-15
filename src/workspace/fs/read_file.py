def read_file(
    path: str, from_line: int | None = None, to_line: int | None = None
) -> str:
    with open(path, "r") as f:
        if from_line is None and to_line is None:
            return f.read()
        elif from_line is not None and to_line is None:
            return "".join(f.readlines()[from_line - 1 :])
        elif from_line is None and to_line is not None:
            return "".join(f.readlines()[:to_line])
        else:
            return "".join(f.readlines()[from_line - 1 : to_line])
