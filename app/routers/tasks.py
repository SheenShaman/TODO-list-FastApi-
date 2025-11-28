from fastapi import APIRouter, Depends

from app import schemas
from app.dependencies import get_current_user
from app.models import Users
from app.repositories.tasks import TasksRepo
from app.routers.exceptions import TasksNotFoundException

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate, user: Users = Depends(get_current_user)
) -> schemas.Task:
    return await TasksRepo.create(title=task.title, user_id=user.id)


@router.get("/all", response_model=list[schemas.Task])
async def get_tasks(
    user: Users = Depends(get_current_user),
) -> list[schemas.Task]:
    return await TasksRepo.get_all_by_kwargs(user_id=user.id)


@router.get("/get_one_by_id/{task_id}", response_model=schemas.Task)
async def get_task_by_id(task_id: int) -> schemas.Task:
    task = await TasksRepo.get_one_by_id(id_=task_id)
    if not task:
        raise TasksNotFoundException
    return task


@router.put("/update_by_id/{task_id}", response_model=schemas.Task)
async def update_task_by_id(
    task_id: int, updated_task: schemas.TaskUpdate
) -> schemas.Task:
    task = await TasksRepo.get_one_by_id(id_=task_id)
    if not task:
        raise TasksNotFoundException
    return await TasksRepo.update_by_id(
        id_=task_id, **updated_task.model_dump(exclude_unset=True)
    )


@router.delete("/delete_by_id/{task_id}", status_code=204)
async def delete_task_by_id(task_id: int) -> None:
    await TasksRepo.delete_by_id(id_=task_id)
