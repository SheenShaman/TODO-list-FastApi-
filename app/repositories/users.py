from app.models import Users
from app.repositories.base import BaseRepo


class UsersRepo(BaseRepo):
    model = Users
