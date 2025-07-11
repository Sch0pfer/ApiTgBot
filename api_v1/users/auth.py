from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX, AuthXConfig

from api_v1.users import UserLogin
from core.models import User

from passlib.context import CryptContext

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


async def login(credentials: UserLogin, db: AsyncSession):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = await db.execute(select(User).where(User.username == credentials.username))
    user = user.scalar_one_or_none()

    if not user or not pwd_context.verify(
        credentials.password, str(user.hashed_password)
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    token = security.create_access_token(uid=str(user.id))

    return {"access_token": token}


async def protected(): ...
