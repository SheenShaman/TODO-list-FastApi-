from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserCreate(User):
    ...


class UserUpdate(User):
    email: str | None = None


class Task(BaseModel):
    title: str


class TaskCreate(BaseModel):
    ...


class TaskUpdate(BaseModel):
    title: str | None = None
