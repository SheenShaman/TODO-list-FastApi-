from pydantic import BaseModel


class User(BaseModel):
    email: str


class UserCreate(User): ...


class UserAuth(User):
    password: str


class UserUpdate(User):
    email: str | None = None
