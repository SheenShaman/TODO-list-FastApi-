from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.database import get_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/all", response_model=list[schemas.User])
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(models.Users))
    return result.scalars().all()


@router.get("/get_one_by_id/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    query = select(models.Users).where(models.Users.id == user_id)
    user = (await db.execute(query)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update_by_id/{user_id}", response_model=schemas.User)
async def update_user_by_id(user_id: int, updated_user: schemas.UserUpdate, db: AsyncSession = Depends(get_session)):
    query = select(models.Users).where(models.Users.id == user_id)
    user = (await db.execute(query)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/delete_by_id/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    query = select(models.Users).where(models.Users.id == user_id)
    user = (await db.execute(query)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
