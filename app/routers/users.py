from fastapi import APIRouter, Response
from fastapi.params import Depends

from app import auth, constants, dependencies, exceptions, schemas
from app.repositories.users import UsersRepo

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    return await UsersRepo.create(**user.model_dump(exclude_unset=True))


@router.get("/all", response_model=list[schemas.User])
async def get_users(
    current_user: schemas.User = Depends(dependencies.get_current_admin_user),
) -> list[schemas.User]:
    return await UsersRepo.get_all()


@router.get("/get_one_by_id/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int) -> schemas.User:
    user = await UsersRepo.get_one_by_id(id_=user_id)
    if not user:
        raise exceptions.UserNotFoundException
    else:
        return user


@router.put("/update_by_id/{user_id}", response_model=schemas.User)
async def update_user_by_id(
    user_id: int, updated_user: schemas.UserUpdate
) -> schemas.User:
    user = await UsersRepo.get_one_by_id(id_=user_id)
    if not user:
        raise exceptions.UserNotFoundException
    else:
        return await UsersRepo.update_by_id(
            id_=user_id, **updated_user.model_dump(exclude_unset=True)
        )


@router.delete("/delete_by_id/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int) -> None:
    await UsersRepo.delete_by_id(id_=user_id)


@router.post("/register")
async def register_user(user: schemas.UserAuth):
    existing_user = await UsersRepo.get_one_by_kwargs(email=user.email)
    if existing_user:
        raise exceptions.UserAlreadyExistsException
    hashed_password = auth.get_password_hash(user.password)
    await UsersRepo.create(email=user.email, password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user: schemas.UserAuth):
    user = await auth.authenticate_user(
        email=user.email, password=user.password
    )
    if not user:
        raise exceptions.IncorrectEmailOrPasswordException
    access_token = auth.create_access_token({"sub": str(user.id)})
    response.set_cookie(
        constants.USER_ACCESS_TOKEN, access_token, httponly=True
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(constants.USER_ACCESS_TOKEN)


@router.get("/me")
async def get_user_me(
    current_user: schemas.User = Depends(dependencies.get_current_user),
):
    return current_user
