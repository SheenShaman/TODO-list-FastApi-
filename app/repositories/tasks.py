from app.db.postgres.models import Tasks
from app.repositories.base import BaseRepo


class TasksRepo(BaseRepo):
    model = Tasks
