from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.database import get_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_session)):
    new_task = models.Tasks(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/all", response_model=list[schemas.Task])
async def get_tasks(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Tasks))
    return result.scalars().all()


@router.get("/get_one_by_id/{task_id}", response_model=schemas.Task)
async def get_task_by_id(task_id: int, db: AsyncSession = Depends(get_session)):
    query = select(models.Tasks).where(models.Tasks.id == task_id)
    task = (await db.execute(query)).scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/update_by_id/{task_id}", response_model=schemas.Task)
async def update_task_by_id(task_id: int, updated_task: schemas.TaskUpdate, db: AsyncSession = Depends(get_session)):
    query = select(models.Tasks).where(models.Tasks.id == task_id)
    task = await db.execute(query)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/delete_by_id/{task_id}", status_code=204)
async def delete_task_by_id(task_id: int, db: AsyncSession = Depends(get_session)):
    query = select(models.Tasks).where(models.Tasks.id == task_id)
    task = await db.execute(query)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
