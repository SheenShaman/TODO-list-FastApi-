from pydantic import BaseModel

class Note(BaseModel):
    title: str
    content: str
    user_id: int
    task_id: int | None = None

class NoteCreate(BaseModel):
    ...
