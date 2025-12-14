from pydantic import BaseModel


class Task(BaseModel):
    title: str
    user_id: int


class TaskCreate(Task): ...


class TaskUpdate(Task):
    title: str | None = None