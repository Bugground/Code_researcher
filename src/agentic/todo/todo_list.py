from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    """The id of the todo item."""

    content: str
    """The content of the todo item."""

    is_done: bool = False
    """Whether the todo item is done."""


class TodoList(BaseModel):
    items: list[TodoItem] = []
    _id_counter: int = 0

    def add_todo(self, todo: str):
        item = TodoItem(
            id=self._next_id(),
            content=todo,
        )
        self.items.append(item)

    def remove_todo(self, id: str):
        for item in self.items:
            if item.id == id:
                self.items.remove(item)
                break

    def clear(self):
        self.items = []

    def mark_todo_as_done(self, id: str):
        for item in self.items:
            if item.id == id:
                item.is_done = True
                break

    def to_markdown(self) -> str:
        content = ""
        if len(self.items) == 0:
            content = "(empty)\n\n> Should call the `add_todo()` tool immediately to add TODO items as a your first plan."
        else:
            for item in self.items:
                content += f"- [{'x' if item.is_done else ' '}] #{item.id}: {item.content.replace('\n', ' | ')}\n"
        return f"""# Todo List

{content}

> Never ever forget to call the `mark_todo_as_done()` tool to update the status.
> Always call the `add_todo()` tool to update the plan before you start working on it."""

    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter


def create_todo_list() -> TodoList:
    return TodoList(items=[])
