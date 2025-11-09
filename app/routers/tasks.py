from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=schemas.Task)
async def create_task(task: schemas.Task, db: Session = Depends(get_db)):
    new_task = models.Tasks(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/all", response_model=list[schemas.Task])
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Tasks).all()


@router.get("/get_one_by_id/{task_id}", response_model=schemas.Task)
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/update_by_id/{task_id}", response_model=schemas.Task)
async def update_task_by_id(task_id: int, updated_task: schemas.Task, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.post("/delete_by_id/{task_id}")
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
