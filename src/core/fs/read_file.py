def read_file(path: str, line_range: tuple[int, int] | None = None) -> str:
    with open(path, "r") as f:
        if line_range is None:
            return f.read()
        else:
            return "".join(f.readlines()[line_range[0] - 1 : (line_range[1])])
