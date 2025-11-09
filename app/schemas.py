from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str


class Task(BaseModel):
    id: int
    title: str
