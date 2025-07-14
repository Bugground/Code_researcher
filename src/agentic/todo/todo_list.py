from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    """The id of the todo item."""

    title: str
    """The title of the todo item."""

    is_done: bool = False
    """Whether the todo item is done."""


class TodoList(BaseModel):
    items: list[TodoItem] = []
    id_counter: int = 0

    def add_todo(self, title: str):
        self.id_counter += 1
        item = TodoItem(
            id=self.id_counter,
            title=title,
        )
        self.items.append(item)

    def clear(self):
        self.items = []

    def remove_todo(self, id: int):
        self.items.pop(id - 1)

    def mark_todo_as_done(self, id: int):
        self.items[id - 1].is_done = True

    def to_markdown(self) -> str:
        content = ""
        if len(self.items) == 0:
            content = "(empty)\n\n> Should call the `add_todo` tool immediately to add Todo items as a your first plan."
        else:
            for item in self.items:
                content += f"- [{'x' if item.is_done else ' '}] #{item.id}: {item.title.replace('\n', ' | ')}\n"
        return f"""# Todo List


{content}
> Never ever forget to call the `mark_todo_as_done()` tool to update the status.
> Always call the `add_todo()` tool to update the plan before you start working on it."""


def create_todo_list() -> TodoList:
    return TodoList(items=[])
