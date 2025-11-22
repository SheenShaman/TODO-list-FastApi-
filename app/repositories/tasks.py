from app.repositories import BaseRepo
from app.models import Tasks


class TasksRepo(BaseRepo):
    model = Tasks
