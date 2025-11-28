from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str


class UserCreate(User): ...


class UserAuth(User):
    password: str


class UserUpdate(User):
    email: str | None = None


class Task(BaseModel):
    title: str
    user_id: int


class TaskCreate(Task): ...


class TaskUpdate(Task):
    title: str | None = None
