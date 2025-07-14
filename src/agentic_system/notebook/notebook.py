from pydantic import BaseModel


class Note(BaseModel):
    content: str


class Notebook(BaseModel):
    notes: list[Note]

    def add_note(self, note_content: str):
        note = Note(content=note_content)
        self.notes.append(note)

    def clear(self):
        self.notes = []

    def to_markdown(self) -> str:
        if len(self.notes) == 0:
            return "# Notebook\n\n(empty)\n\n> Should call the `add_note()` tool immediately to add your first note."
        else:
            return f"# Notebook\n\n{'\n\n'.join([note.content for note in self.notes])}"


def create_notebook() -> Notebook:
    return Notebook(notes=[])
