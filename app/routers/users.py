from fastapi import APIRouter, HTTPException
from app import schemas
from app.repositories.users import UsersRepo

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    return await UsersRepo.create(**user.model_dump(exclude_unset=True))


@router.get("/all", response_model=list[schemas.User])
async def get_users() -> list[schemas.User]:
    return await UsersRepo.get_all()


@router.get("/get_one_by_id/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int) -> schemas.User:
    user = await UsersRepo.get_one_by_id(id_=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.put("/update_by_id/{user_id}", response_model=schemas.User)
async def update_user_by_id(user_id: int, updated_user: schemas.UserUpdate) -> schemas.User:
    user = await UsersRepo.get_one_by_id(id_=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return await UsersRepo.update_by_id(id_=user_id, **updated_user.model_dump(exclude_unset=True))


@router.delete("/delete_by_id/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int) -> None:
    await UsersRepo.delete_by_id(id_=user_id)
