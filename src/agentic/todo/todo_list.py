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

    def add_todo(self, id: int, title: str):
        item = TodoItem(
            id=id,
            title=title,
        )
        self.items.append(item)

    def clear(self):
        self.items = []

    def remove_todo(self, id: int):
        for item in self.items:
            if item.id == id:
                self.items.remove(item)
                break

    def mark_todo_as_done(self, id: int):
        for item in self.items:
            if item.id == id:
                item.is_done = True
                break

    def to_markdown(self) -> str:
        content = ""
        if len(self.items) == 0:
            content = "(empty)\n\n> Should call the `add_todo` tool immediately to add Todo items as a your first plan."
        else:
            for item in self.items:
                content += f"- [{'x' if item.is_done else ' '}] #{item.id}: {item.title.replace('\n', ' | ')}\n"
        return f"# Todo List\n\n{content.strip()}\n\n> Never ever forget to call the `mark_todo_as_done()` tool to update the status."


def create_todo_list() -> TodoList:
    return TodoList(items=[])
