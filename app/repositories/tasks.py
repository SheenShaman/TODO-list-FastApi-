from app.models import Tasks
from app.repositories.base import BaseRepo


class TasksRepo(BaseRepo):
    model = Tasks
