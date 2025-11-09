from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Tasks:
    """
    Tasks
    """

    @router.post("/create", response_model=schemas.Task)
    async def create_task(self, task: schemas.Task, db: Session = Depends(get_db)):
        query = models.Tasks(title=task.title)
        db.add(query)
        db.commit()
        db.refresh(query)
        return query

    @router.get("/all", response_model=list[schemas.Task])
    async def get_tasks(self, db: Session = Depends(get_db)):
        return db.query(models.Tasks).all()

    @router.get("/get_one_by_id/{task_id}", response_model=schemas.Task)
    async def get_task_by_id(self, task_id: int, db: Session = Depends(get_db)):
        query = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
        if not query:
            raise HTTPException(status_code=404, detail="Task not found")
        return query

    @router.post("/update_by_id/{task_id}", response_model=schemas.Task)
    async def update_task_by_id(self, task_id: int, new_title: str):
        task = self.get_task_by_id(task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            task.title = new_title
            return task

    @router.post("/delete_by_id/{task_id}")
    async def delete_task_by_id(self, task_id: int, db: Session = Depends(get_db)):
        task = self.get_task_by_id(task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            db.delete(task)
            db.commit()
            db.refresh(task)

