from datetime import datetime, timedelta

from asyncpg.pgproto.pgproto import timedelta
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from app.config import settings

load_dotenv()

from app import schemas
from app.repositories.users import UsersRepo

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.JWT_ENCODE_KEY, settings.JWT_ALGORITHM
    )
    return encode_jwt


async def authenticate_user(email: str, password: str) -> schemas.User | None:
    user = await UsersRepo.get_one_by_kwargs(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user
