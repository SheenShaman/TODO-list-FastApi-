from app.repositories import BaseRepo
from app.models import Users


class UsersRepo(BaseRepo):
    model = Users
