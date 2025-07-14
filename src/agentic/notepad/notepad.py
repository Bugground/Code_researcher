from pydantic import BaseModel


class Note(BaseModel):
    content: str


class Notepad(BaseModel):
    notes: list[Note]

    def add_note(self, note_content: str):
        note = Note(content=note_content)
        self.notes.append(note)

    def clear(self):
        self.notes = []

    def to_markdown(self) -> str:
        content = ""
        if len(self.notes) == 0:
            content = "(empty)\n\n> Should call the `add_note()` tool immediately to add your first note."
        else:
            for note in self.notes:
                content += f"## {note.content}\n\n"
        return f"# Notepad\n\n{content}"


def create_notepad() -> Notepad:
    return Notepad(notes=[])
