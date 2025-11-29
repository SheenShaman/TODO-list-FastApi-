from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app import config, constants, exceptions, schemas
from app.repositories.users import UsersRepo


def get_token(request: Request):
    token = request.cookies.get(constants.USER_ACCESS_TOKEN)
    if not token:
        raise exceptions.TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> schemas.User:
    try:
        payload = jwt.decode(
            token, config.settings.JWT_ENCODE_KEY, config.settings.JWT_ALGORITHM
        )
    except JWTError:
        raise exceptions.IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise exceptions.TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise exceptions.UserNotFoundException
    user = await UsersRepo.get_one_by_id(int(user_id))
    if not user:
        raise exceptions.UserNotFoundException
    return user


async def get_current_admin_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if current_user.role != constants.ADMIN_ROLE:
        raise exceptions.UserNotAdminException
    return current_user
