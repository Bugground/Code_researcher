from pydantic import BaseModel


class Note(BaseModel):
    content: str


class Notepad(BaseModel):
    notes: list[Note]

    def add_note(self, content: str):
        self.notes.append(Note(content=content))

    def to_markdown(self) -> str:
        content = ""
        if len(self.notes) == 0:
            content = "(empty)\n\n> Should call the `add_note` tool immediately to add your first note."
        else:
            for note in self.notes:
                content += f"{note.content}\n\n"
            content += "> Should call the `add_note` tool immediately to note your findings in each step."
        return f"# Notepad\n\n{content}"
